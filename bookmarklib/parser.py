from __future__ import annotations
from queue import Queue
from bs4 import BeautifulSoup, PageElement, Tag
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Bookmark:
  name: str
  url: str
  add_date: datetime | None
  last_modified: datetime | None

@dataclass
class BookmarkFolder:
  name: str
  children: list[BookmarkFolder | Bookmark]
  add_date: datetime | None
  last_modified: datetime | None

@dataclass
class BookmarkRoot:
  children: list[BookmarkFolder | Bookmark]
  
def parse_bookmarks_firefox(html: str)-> BookmarkRoot:
  html = html.replace("<DT>", "")
  html = html.replace("<p>", "")  

  parsed_html = BeautifulSoup(html, 'lxml')
  root_tag = parsed_html.findChild("dl")
  assert isinstance(root_tag, Tag)

  bookmark_root: BookmarkRoot = BookmarkRoot(children=[])
  bookmark_queue: Queue = Queue()
  
  
  
  def init_queue():
    child_h3_list: list[Tag] = list(root_tag.find_all("h3", recursive=False))
    child_dl_list: list[Tag] = list(root_tag.find_all("dl", recursive=False))
    child_a_list: list[Tag] = list(root_tag.find_all("a", recursive=False))
    

    for h3, dl in zip(child_h3_list, child_dl_list):
      
      name = h3.text      
      if (add_date := h3.attrs.get("add_date")) == None:
        print("Unable to find add_date for folder")
      else:
        add_date = datetime.utcfromtimestamp(float(add_date))
      
      if (last_modified := h3.attrs.get("last_modified")) == None:
        print("Unable to find last_modified for folder")
      else:
        last_modified = datetime.utcfromtimestamp(float(last_modified))
      
      bookmark_folder = BookmarkFolder(
        name=name,
        children=[],
        add_date=add_date,
        last_modified=last_modified
      )
      bookmark_root.children.append(bookmark_folder)
      bookmark_queue.put((bookmark_folder, dl))
    
    for a in child_a_list:
      name = a.text
      
      if (add_date := a.attrs.get("add_date")) == None:
        print("Unable to find add_date for folder")
      else:
        add_date = datetime.utcfromtimestamp(float(add_date))
      
      if (last_modified := a.attrs.get("last_modified")) == None:
        print("Unable to find last_modified for folder")
      else:
        last_modified = datetime.utcfromtimestamp(float(last_modified))

      if (url := a.attrs.get("href")) == None:
        print("Unable to find url for bookmark")
        url = "localhost"
  
      bookmark = Bookmark(
        name=name,
        url=url,
        add_date=add_date,
        last_modified=last_modified
      )
      bookmark_root.children.append(bookmark)
    
  init_queue()
  

  

  while not bookmark_queue.empty():
    item = bookmark_queue.get()
    parent_folder: BookmarkFolder = item[0]
    parent_tag: Tag = item[1]
    
    child_h3_list: list[Tag] = list(parent_tag.find_all("h3", recursive=False))
    child_dl_list: list[Tag] = list(parent_tag.find_all("dl", recursive=False))
    child_a_list: list[Tag] = list(parent_tag.find_all("a", recursive=False))
    
    for h3, dl in zip(child_h3_list, child_dl_list):
      name = h3.text      
      if (add_date := h3.attrs.get("add_date")) == None:
        print("Unable to find add_date for folder")
      else:
        add_date = datetime.utcfromtimestamp(float(add_date))
      
      if (last_modified := h3.attrs.get("last_modified")) == None:
        print("Unable to find last_modified for folder")
      else:
        last_modified = datetime.utcfromtimestamp(float(last_modified))
      
      child_folder = BookmarkFolder(
        name=name,
        children=[],
        add_date=add_date,
        last_modified=last_modified
      )
      parent_folder.children.append(child_folder)
      bookmark_queue.put((child_folder, dl))
    
    for a in child_a_list:
      name = a.text
      
      if (add_date := a.attrs.get("add_date")) == None:
        print("Unable to find add_date for folder")
      else:
        add_date = datetime.utcfromtimestamp(float(add_date))
      
      if (last_modified := a.attrs.get("last_modified")) == None:
        print("Unable to find last_modified for folder")
      else:
        last_modified = datetime.utcfromtimestamp(float(last_modified))

      if (url := a.attrs.get("href")) == None:
        print("Unable to find url for bookmark")
        url = "localhost"
  
      bookmark = Bookmark(
        name=name,
        url=url,
        add_date=add_date,
        last_modified=last_modified
      )
      parent_folder.children.append(bookmark)
  

  
  return bookmark_root

  



