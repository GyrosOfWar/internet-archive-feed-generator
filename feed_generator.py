from internetarchive import search_items, Item
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone


# 5/29/2015
def parse_date(date: str) -> datetime:
    return datetime.strptime(date, "%m/%d/%Y").replace(tzinfo=timezone.utc)


def get_stream_url(identifier: str, file_name: str) -> str:
    return f"https://archive.org/serve/{identifier}/{file_name}"


def add_feed_items(feed: FeedGenerator):
    results = search_items('subject:"The Giant Beastcast (Premium)"')
    iterator = results.iter_as_items()
    for item in iterator:
        mp3_files = [file for file in item.files if file["name"].endswith(".mp3")]
        if len(mp3_files) == 0:
            continue
        mp3_file = mp3_files[0]
        mp3_link = get_stream_url(item.identifier, mp3_file["name"])
        file_size = mp3_file["size"]

        feed_item = feed.add_entry()
        feed_item.id(item.metadata["external-identifier"])
        feed_item.link(href=f"https://archive.org/details/{item.identifier}")
        feed_item.author({"name": item.metadata["creator"]})
        feed_item.description(item.metadata["description"])
        feed_item.title(item.metadata["title"])
        feed_item.pubDate(parse_date(item.metadata["date"]))
        feed_item.enclosure(url=mp3_link, length=file_size, type="audio/mp3")


def generate_feed() -> FeedGenerator:
    feed = FeedGenerator()
    feed.title("The Giant Beastcast")
    feed.link(href="https://www.giantbomb.com")
    feed.image(
        url="https://www.giantbomb.com/a/uploads/original/11/110673/2894068-3836779617-28773.png",
        width="144",
        height="144",
    )
    feed.description(
        "The Giant Bomb East team gathers to talk about the week in video games, their lives, and basically anything that interests them. All from New York City!"
    )

    add_feed_items(feed)
    return feed


if __name__ == "__main__":
    print("generating feed, this might take a while")
    feed = generate_feed()
    with open("feed.xml", "w") as fp:
        fp.write(feed.rss_str())
    print("wrote RSS feed to feed.xml")
