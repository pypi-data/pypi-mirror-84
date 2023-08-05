import os
from datetime import datetime

import pytest
import requests
import responses
from polygon import RESTClient
from polygon.rest.models import StocksEquitiesAggregatesApiResponse

from polygon_cache.cache import CachedRESTClient
from polygon_cache.tests import expected_values


@pytest.fixture
def create_client(tmpdir):
    temp = str(tmpdir.join("polygon-cache"))
    return CachedRESTClient("api_key", cache_location=temp)


@pytest.fixture
def fake_json_request_on_2020_01_17(tmp_path, freezer):
    def _fake_request(json_data: dict):
        freezer.move_to("2020-01-17")
        temp = str(tmp_path)
        responses.add(responses.GET, "http://url.com", json=json_data)
        resp = requests.get("http://url.com")
        client = CachedRESTClient("api_key", cache_location=temp)
        return resp, client

    return _fake_request


def test_cache_creation(tmpdir):
    temp = str(tmpdir.join("polygon-cache"))
    CachedRESTClient("api_key", cache_location=temp)
    assert os.path.isfile(temp + ".sqlite")


@pytest.mark.parametrize(
    "date,expected_filter_response",
    [("2020-01-15", True), ("2020-01-17", False), ("2020-01-30", False)],
)
@responses.activate
def test_cache_filter_from(
    date, expected_filter_response, fake_json_request_on_2020_01_17
):
    data = {"from": date}
    resp, client = fake_json_request_on_2020_01_17(data)
    assert client._cache_filter(resp) is expected_filter_response


@pytest.mark.parametrize(
    "unix_ms,expected_filter_response",
    [(1579107600000, True), (1579280400000, False), (1580403600000, False)],
)
@responses.activate
def test_cache_filter_unix_timestamps(
    unix_ms, expected_filter_response, fake_json_request_on_2020_01_17
):
    data = {"results": [{"t": "not this one"}, {"t": unix_ms}]}
    resp, client = fake_json_request_on_2020_01_17(data)
    assert client._cache_filter(resp) is expected_filter_response


@pytest.mark.parametrize(
    "day1,day2,interval,expected_dates",
    [
        (
            datetime(2020, 1, 1),
            datetime(2020, 1, 14),
            5,
            [
                (datetime(2020, 1, 1, 0, 0), datetime(2020, 1, 6, 0, 0)),
                (datetime(2020, 1, 7, 0, 0), datetime(2020, 1, 12, 0, 0)),
                (datetime(2020, 1, 13, 0, 0), datetime(2020, 1, 14, 0, 0)),
            ],
        ),
        (
            datetime(2020, 1, 1),
            datetime(2020, 1, 14),
            3000,
            [(datetime(2020, 1, 1, 0, 0), datetime(2020, 1, 14, 0, 0))],
        ),
    ],
)
def test_calculate_aggregate_api_calls(
    day1, day2, interval, expected_dates, create_client
):
    client = create_client
    assert client._calculate_aggregate_api_calls(day1, day2, interval) == expected_dates


def create_fake_aggv2_results(
    number_of_results: int = 50,
    ticker_symbol: str = "TIC",
    volume_initial: int = 1000,
    open_initial: float = 100,
    close_initial: float = 105,
    high_initial: float = 110,
    low_initial: float = 95,
    unix_msec_timestamp_initial: int = 100000,
    number_of_items_in_aggregate_window: float = 5,
):
    results = []
    for i in range(0, number_of_results):
        result = {
            "T": ticker_symbol,
            "v ": volume_initial + i,
            "o": open_initial + i,
            "c": close_initial + i,
            "h": high_initial + i,
            "l": low_initial + i,
            "t": unix_msec_timestamp_initial + i * 10,
            "n": number_of_items_in_aggregate_window + i,
        }
        results.append(result)

    return results


@pytest.fixture
def create_fake_stocks_equities_aggregate_api_response():
    def _create_fake_stocks_equities_aggregate_api_response(
        ticker: str = "TIC",
        status: str = "OK",
        adjusted: bool = True,
        queryCount: int = 100,
        resultsCount: int = 50,
        results=create_fake_aggv2_results,
    ):
        api_response = StocksEquitiesAggregatesApiResponse()
        api_response.ticker = ticker
        api_response.status = status
        api_response.adjusted = adjusted
        api_response.queryCount = queryCount
        api_response.resultsCount = resultsCount
        api_response.results = results()

        return api_response

    return _create_fake_stocks_equities_aggregate_api_response


def test_aggregate_call(
    mocker, create_fake_stocks_equities_aggregate_api_response, create_client
):
    mock = mocker.patch.object(RESTClient, "stocks_equities_aggregates")
    mock.return_value = create_fake_stocks_equities_aggregate_api_response()
    client = create_client
    combined_results = client.stocks_equities_aggregates(
        "TIC", 1, "minute", "2020-06-04", "2020-06-20"
    )

    assert combined_results.__dict__ == expected_values.AGGREGATES_TEST


@pytest.fixture
def empty_class():
    class EmptyClass:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    return EmptyClass


def test_const_attr_combine(create_client, empty_class):
    client = create_client
    combined = client._combine_aggregate_results(
        [empty_class(status=True), empty_class(status=True)],
        ["status"],
        [],
        [],
        empty_class,
    )
    assert combined.status is True


def test_value_error_multiple_constant_attrs_combine_aggregate_results(
    create_client, empty_class
):
    client = create_client
    with pytest.raises(ValueError) as error:
        client._combine_aggregate_results(
            [empty_class(status=True), empty_class(status=False)],
            ["status"],
            [],
            [],
            empty_class,
        )

    assert (
        "Multiple status encountered while trying to combine results: False and True"
        in str(error)
    )


def test_combine_aggregate_results_summed(create_client, empty_class):
    client = create_client
    api_responses = [empty_class(number=value) for value in [20, 30, 50]]

    combined = client._combine_aggregate_results(
        api_responses, [], ["number"], [], empty_class
    )

    assert combined.number == 100


def test_combine_aggregate_results_combined(create_client, empty_class):
    client = create_client
    thing1 = empty_class(stuff=[1, "thing"])
    thing2 = empty_class(stuff=[{"hello": "hi"}])

    combined = client._combine_aggregate_results(
        [thing1, thing2], [], [], ["stuff"], empty_class
    )

    assert combined.stuff == [1, "thing", {"hello": "hi"}]
