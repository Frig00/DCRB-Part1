import os
import wikipediaapi
import re

# Download the content of a Wikipedia page
def wiki_download(save_path, content):
    if not os.path.exists(save_path):
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Content saved to {save_path} successfully.")

num_cat = {}

# Search for the content of Wikipedia music category and create directories for categories and files for pages
def wiki_search(categorymembers, wiki_wiki, path='', level=0, max_level=5):
    if path not in num_cat:
        num_cat[path] = 0

    num_files = 0

    for c in categorymembers.values():

        if (c.ns != wikipediaapi.Namespace.CATEGORY and num_files > 2) or (c.ns == wikipediaapi.Namespace.CATEGORY and num_cat[path] > 2):
            continue

        print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))

        category = c.title.split(":")[-1]

        if c.ns == wikipediaapi.Namespace.CATEGORY and (not os.path.exists(os.path.join(path, category))):
            os.makedirs(os.path.join(path, category))
            num_cat[path] += 1


        if c.ns != wikipediaapi.Namespace.CATEGORY:
            page = wiki_wiki.page(c.title)

            pattern = r'[<>:"\\|?*/]'
            page_title = re.sub(pattern, '-', c.title) if re.search(pattern, c.title) else c.title

            save_path = os.path.join(path, page_title + '.txt')
            wiki_download(save_path, page.text)
            num_files += 1

        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            wiki_search(c.categorymembers, wiki_wiki, path=os.path.join(path, category), level=level + 1, max_level=max_level)


if __name__ == "__main__":

    wiki_wiki = wikipediaapi.Wikipedia('DCRB (andrea.frigatti00@gmail.com)', 'en', extract_format=wikipediaapi.ExtractFormat.WIKI)
    cat = wiki_wiki.page("Category:Music")
    directory = "DCRB"
    if not os.path.exists(directory):
        os.makedirs(directory)
    wiki_search(cat.categorymembers, wiki_wiki, path=directory)