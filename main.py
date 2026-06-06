import utils.graphql_interface as graphql_interface

test_query_file_path = "queries/test_query.graphql"

test_query = graphql_interface.get_query_from_file_path(test_query_file_path)

response = graphql_interface.run_anilist_query(
    test_query,
    {
        "type": "ANIME",
        "userName": "turbogames",
        "status": "CURRENT"
    }
)

for entry in response["MediaListCollection"]["lists"][0]["entries"]:
    entry_title = entry["media"]["title"]["english"]

    if entry_title == None:
        entry_title = entry["media"]["title"]["romaji"]

    if entry_title == None:
        entry_title = entry["media"]["title"]["native"]

    entry_progress = entry["progress"]
    entry_episodes = entry["media"]["episodes"]

    if entry_episodes == None:
        entry_episodes = max(entry_progress, 12)

    print(f"{entry_title} ({entry_progress}/{entry_episodes})")



