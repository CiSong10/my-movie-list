import json

import requests
from flask import Flask, render_template, request


BASE_URL = 'http://www.omdbapi.com/'
KEY = '12f31693'
MOVIE_FILE = 'watching_list.txt'


class TreeNode:
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        if isinstance(val, list):
            self.val = val
        else:
            self.val = [val]
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self,key,value,lc,rc):
        self.key = key
        self.val = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def put(self, key, val):
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)

    def _put(self, key, val, currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key, val, parent=currentNode)
        elif key == currentNode.key:
            currentNode.val.append(val)
        else:
            if currentNode.hasRightChild():
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, val, parent=currentNode)

    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.val
            else:
                return None
        else:
            return None

    def _get(self, key, currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key, currentNode.leftChild)
        else:
            return self._get(key, currentNode.rightChild)

    def __getitem__(self, key):
        return self.get(key)


traverse_list = []
def traverse(root):
    if not root:
        return
    traverse_list.append(root.val)
    traverse(root.leftChild)
    traverse(root.rightChild)
    return traverse_list


def yes(prompt):
    answer = input(prompt)
    if answer in ['yes', 'y']:
        return True
    elif answer in ['no', 'n']:
        return False


def get_movie(MovieTree, title):
    params = {'s': title, 'apikey': KEY}
    movies_json = requests.get(BASE_URL, params).json()
    movies = movies_json['Search']
    for movie in movies:
        check_movie = yes(f'Is "{movie["Title"]}" the movie you are looking for?')
        if check_movie:
            MovieTree.put(int(movie["Year"]), movie)
            print(f'"{movie["Title"]}" has been stored into your watching list!')
            break


def saveTree(tree, treeFile):
    if isinstance(tree, BinarySearchTree):
        node = tree.root
    elif not tree:
        return None
    else:  # tree is TreeNode()
        node = tree
    print(node.key, file=treeFile)
    for movie_json in node.val:
        print(movie_json, file=treeFile)
    saveTree(node.leftChild, treeFile)
    saveTree(node.rightChild, treeFile)


def loadTree(treeFile):
    newtree = BinarySearchTree()
    while True:
        line = treeFile.readline().strip()
        if line == '':
            break
        elif line.isdigit():
            int(line)
            key = int(line)
            # movie_json_list = []
        else:
            # line = line.replace('\'', '\"')
            movie = json.loads(json.dumps(eval(line)))
            newtree.put(key, movie)
    # print(newtree.root.val)
    return newtree


def main():
    if yes('Would you like to load a watching list from a file?'):
        treeFile = open(MOVIE_FILE, 'r')
        MovieTree = loadTree(treeFile)
        treeFile.close()
    else:
        MovieTree = BinarySearchTree()
    # print(MovieTree.root.val)
    title = input("What movie would you like to add to the watching list: ")
    get_movie(MovieTree, title)
    # print(MovieTree.root.rightChild.val)

    movie_file = open(MOVIE_FILE, 'w')
    saveTree(MovieTree, movie_file)
    movie_file.close()
    print('The file has been saved.')


app = Flask(__name__)


@app.route('/')
def index():
    # iterate over tree
    all_movie_titles = []
    traverse_list = traverse(MovieTree.root)
    for year_movies_list in traverse_list:
        for movie in year_movies_list:
            all_movie_titles.append(movie['Title'])
    return render_template('index.html',all_movie_titles=all_movie_titles)


@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    movie_title = request.form['movie']
    params = {'s': movie_title, 'apikey': KEY}
    movie = requests.get(BASE_URL, params).json()['Search'][0]
    movie_title = movie['Title']
    movie_year = int(movie['Year'])
    MovieTree.put(movie_year, movie)
    movie_file = open(MOVIE_FILE, 'w')
    saveTree(MovieTree, movie_file)
    movie_file.close()
    return render_template('handle_form.html', movie_title = movie_title)


@app.route('/movie_detail', methods=['POST'])
def movie_detail():
    year = int(request.form['year'])
    year_movie_list = MovieTree.get(year)
    return render_template('movie_detail.html', year = year, year_movie_list=year_movie_list)


if __name__ == '__main__':
    treeFile = open(MOVIE_FILE, 'r')
    MovieTree = loadTree(treeFile)
    treeFile.close()

    # main()
    app.run(debug=True)
