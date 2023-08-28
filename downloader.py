from internetarchive import search_items
import sys
import json


def find_download_urls(query: str):
    results = search_items(query)
    iterator = results.iter_as_items()
    for item in iterator:
        mp4_files = list(item.get_files(glob_pattern="*.mp4"))
        if len(mp4_files) == 0:
            continue
        mp4_file = mp4_files[0]
        yield {
            "url": mp4_file.url,
            "title": item.metadata["title"],
            "description": item.metadata["description"],
            "size": mp4_file.size,
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python downloader.py <query>")
        sys.exit(1)
    query = sys.argv[1]
    print("searching for query:", query)
    with open("urls.txt", "w") as fp:
        for file in find_download_urls(query):
            fp.write(json.dumps(file))
            fp.write("\n")
