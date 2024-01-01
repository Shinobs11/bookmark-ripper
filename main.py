
def main(bookmarks_path: str, output_path: str):
  import traceback
  from bs4 import BeautifulSoup
  from lxml.etree import tostring
  from bookmarklib.parser import Bookmark, BookmarkFolder, parse_bookmarks_firefox
  from queue import Queue
  import os





  



  with open("/home/shino/bookmarks.html") as f:
    root = parse_bookmarks_firefox(f.read())
    
    target_path = "/home/shino/dev/bookmark-ripper/output"
    
    q = Queue()
    for i, x in enumerate(root.children):
      q.put((x, target_path, i))
    
    while not q.empty():
      
      item = q.get()
      
      bookmark: BookmarkFolder | Bookmark = item[0]
      parent_path: str = item[1]
      index:int = item[2]
      try:
        if isinstance(bookmark, BookmarkFolder):
          path = os.path.join(parent_path, str(index))
          for i, child in enumerate(bookmark.children):
            q.put((child, path, i))
          os.mkdir(path)
          with open(os.path.join(path, "BOOKMARK_NAME"), mode="w") as f:
            f.write(bookmark.name)
        
        
        elif isinstance(bookmark, Bookmark):
          path = os.path.join(parent_path, str(index))
          os.mkdir(path)
          with open(os.path.join(path, "BOOKMARK_NAME"), mode="w") as f:
            f.write(bookmark.name)
        
      except:
        print("oops")
        print(traceback.format_exc())
  

if __name__ == "__main__":
  import argparse, pathlib, os
  
  
  parser = argparse.ArgumentParser(
    description="""
    bookmark-ripper is a tool to download and backup bookmarked webpages
    """  
  )
  
  parser.add_argument("-b", "--bookmarks", required=True,
                      help="Path to bookmark file.",
                      dest="bookmarks_path",
                      type=pathlib.Path
                      )
  parser.add_argument("-o", "--output", required=True,
                      help="Path to output directory.",
                      dest="output_path",
                      type=pathlib.Path
                      )
  
  
  args = parser.parse_args()
  

  bookmarks_path = os.path.abspath(args.bookmarks_path)
  output_path = os.path.abspath(args.output_path)
  
  main(
    bookmarks_path=bookmarks_path,
    output_path=output_path
  )
  
  
    
    
    
    


  
  