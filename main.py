import utils.graphql_interface as graphql_interface
from utils.entry import Entry
# from utils.media import Media
# from utils.tag_data import TagData
from utils.tag_score import TagScore

test_query_file_path = "queries/test_query.graphql"

test_query = graphql_interface.get_query_from_file_path(test_query_file_path)

response = graphql_interface.run_anilist_query(
    test_query,
    {
        "type": "ANIME",
        "userName": "turbogames"
    }
)

started_entries: list[Entry] = []
not_started_entries: list[Entry] = []

tag_scores: dict[str, TagScore] = {}

for watch_list in response["MediaListCollection"]["lists"]: #[0]["entries"]:
    for raw_entry in watch_list["entries"]:
        entry: Entry = Entry(raw_entry)

        if entry.status == "PLANNING":
            not_started_entries.append(entry)
        else:
            started_entries.append(entry)

for entry in started_entries:
    print(f"[{entry.status}] {entry.media.title} ({entry.progress}/{entry.media.total_episodes})")

    for tag_data in entry.media.tags:
        if tag_data.tag_name not in tag_scores:
            tag_scores[tag_data.tag_name] = TagScore(tag_data.tag_name)

        tag_scores[tag_data.tag_name].add_entry(entry, tag_data)

lowest_tag_score = +10000.0

for tag_score in tag_scores.values():
    if tag_score.total_tag_score > lowest_tag_score:
        continue
    
    lowest_tag_score = tag_score.total_tag_score

    print(f"Tag {tag_score.tag_name} has a score of {tag_score.total_tag_score}")

tag_score = tag_scores["Gender Bending"]

print(f"Tag {tag_score.tag_name} has a score of {tag_score.total_tag_score}")




