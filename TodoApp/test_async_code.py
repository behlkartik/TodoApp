import asyncio

import requests
from time import perf_counter
from pprint import pprint
from aiohttp import ClientSession
import logging
import re
import typing as t
import sys
import json
from urllib import parse
import aiofiles

# async def validate_card_details():
#     print("Validate card details...")
#     await asyncio.sleep(10)   #blocked on i/o operation
#     print("Card details validated...")
#     return {"status": "success", "message": "Card details validated successfully", "number": "123456789"}
#
#
# async def cart_checkout():
#     print("Cart checkout...")
#     await asyncio.sleep(3)
#     return True
#
#
# async def main():
#     print("Order recieved..")
#     card_validation_task = asyncio.create_task(validate_card_details())
#     # print("Go to checkout page")
#     cart_checkout_task = asyncio.create_task(cart_checkout())
#     is_checkout_done = await cart_checkout_task
#     card_validation_value = await card_validation_task
#     if is_checkout_done and card_validation_value:
#         print("Order placed successfully with the below card details", card_validation_value)
    # await cart_checkout_task
    # asyncio.create_task(greet())


# class StockMarketApi:
#     BASE_URL="https://www.alphavantage.co/query?function={}&symbol={}&apikey={}"
#     API_KEY="24211N7HFYC5K3FM"
#
#     def __init__(self, function):
#         self.function = function
#
#     async def get_data(self, symbol):
#         async with ClientSession() as session:
#             print(f"Making api call for symbol {symbol}")
#             response = await session.get(url=self.BASE_URL.format(self.function, symbol, self.API_KEY))
#             response.raise_for_status()
#             return await response.json()
#
#
# async def make_api_call():
#     responses = []
#     for symbol in ["MSFT", "AAPL", "AMZN"]:
#         responses.append(await StockMarketApi("TIME_SERIES_INTRADAY").get_data(symbol))
#     return responses
#
#
# async def main():
#     start = perf_counter()
#     print("Getting all stock prices...")
#     responses = await make_api_call()
#     pprint(responses)
#     print("Done making api calls...")
#     print(f"Total time: {perf_counter() - start}")
#
#
# asyncio.run(main())


logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)
HREF_RE = re.compile(r'href="http.*?"')

urls = [
    "https://regex101.com/",
    "https://docs.python.org/3/this-url-will-404.html",
    "https://www.nytimes.com/guides/",
    "https://www.mediamatters.org/",
    "https://1.1.1.1/",
    "https://www.politico.com/tipsheets/morning-money",
    "https://www.bloomberg.com/markets/economics",
    "https://www.ietf.org/rfc/rfc2616.txt",
]


async def make_api_call(url: str, session: ClientSession):
    logger.info(f"making http call for {url}")
    response = await session.get(url=url)
    logger.info("Got response")
    response_content = await response.text()
    return response_content


def _normalize_parsed_links(content: str):
    content_with_href = HREF_RE.findall(content)
    links_without_href = list(map(lambda link: re.sub("\"$", "", re.sub("^href=\"", "", link)), content_with_href))
    return list(map(lambda link: parse.unquote(link), links_without_href))


async def write_one(url, session):
    links = await parse_link(url, session=session)
    async with aiofiles.open("links.json", "r+") as f:
        logger.info(f"Writing links for url {url}")
        await f.seek(0)
        data = await f.read()
        _data = json.loads(data)
        _data["urls"].append(dict(url=url, links=links))
        await f.seek(0)
        await f.write(json.dumps(_data, indent=4))
    return links


async def parse_link(url: str, session: ClientSession):
    response_html_content = await make_api_call(url, session)
    parsed_urls = _normalize_parsed_links(response_html_content)
    links: t.List[str] = parsed_urls
    logger.info(f"Done parsing links for url {url}")
    return links


async def bulk_parse_links(urls: t.List[str]):
    """
    This code is using asyncio to asynchronously fetch links from multiple URLs concurrently.

    The tasks list is initialized as empty. Then a for loop iterates over the urls list, calling parse_links on each URL and session. This returns a coroutine/Future for each URL.

    The Futures are appended to the tasks list, building up a list of pending asynchronous operations - one for each URL.

    After the loop, asyncio.gather is called with the tasks list unpacked using *. This will wait for all the coroutines in tasks to complete concurrently.

    The await keyword pauses execution until gather finishes, and response will contain the results from each parse_links call.

    So in summary, it:
        1.Loops over URLs
        2.Kicks off an async parse_links for each URL
        3.Gathers all the results together once complete
        4. Waits for the full response
    This allows fetching multiple URLs asynchronously without blocking the main thread, improving performance over synchronous requests.

    """
    async with aiofiles.open("links.json", "w") as f:
        logger.info("Preparing Base file...")
        await f.write(json.dumps({"urls": []}, indent=4))
        logger.info("Done Preparing Base file")

    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(write_one(url, session))   # creating a list of futures/promises
        response = await asyncio.gather(*tasks)                 # waiting till all the futures/promises are resolved
        logger.info(f"Got response for all urls, Response: {json.dumps(response)}")

if __name__ == "__main__":
    start = perf_counter()
    asyncio.run(bulk_parse_links(urls))
    total = perf_counter() - start
    logger.info(f"Total time taken: {total}")