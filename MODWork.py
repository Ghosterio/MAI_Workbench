import tkinter as tk
import itertools
from tkinter import messagebox
import collections
from collections import Counter
import random

def main():
    clear()
    tk.Label(win, text='Отчет Теория Ифнормации', font=('Arial', 20, 'bold')).pack()
    tk.Button(win, text='ТЕОРИЯ ГРАФОВ', command=start_graph).pack()
    tk.Button(win, text='БИНАНРНОЕ ДЕРЕВО (WIP)', command=App).pack()
    tk.Button(win, text='МЕТОДЫ ШЕННОНА-ФЭНО И ХАФФМЕНА', command=start_metod).pack()
    tk.Button(win, text='АЛГОРИТМЫ LZ77, LZ78 И LZSS', command=selalg).pack()
    tk.Button(win, text='НАЖМИ МЕНЯ!', command=coloring, fg='pink', bg='purple').pack()
    tk.Button(win, text='ПОКИНУТЬ ПРОГРАММУ', fg='red', command=lambda: quit()).pack()
    tk.Label(win, text='Лисиченко М.И.', font=('Arial', 10, 'bold')).pack()

def clear():
    for i in win.winfo_children():
        i.destroy()

def coloring():
    color=random.randint(1,900000)
    win.config(bg=f'#{color}')

def start_graph():
    clear()
    tk.Label(win, text='Введите пары вершин (1 2, 2 3, ...)', font=('Arial', 14)).pack()
    tk.Entry(win, textvariable=vertex, width=25).pack()
    tk.Label(win, text='Выберите тип графа', font=('Arial', 14)).pack()
    tk.Radiobutton(win, text='Граф ориентированный', font=('Arial', 10), value=1, variable=orint).pack()
    tk.Radiobutton(win, text='Граф НЕориентированный', font=('Arial', 10), value=2, variable=orint).pack()
    tk.Button(win, text='ЗАПУСК', command=graph).pack()
    tk.Button(win, text='ВЕРНУТЬСЯ В МЕНЮ', fg='blue', command=main).pack()

def graph():
    user_input = vertex.get()
    input_list = user_input.split(',')
    input_list = [item.strip() for item in input_list]
    input_list = [[int(item) for item in pair.split()] for pair in input_list]
    middirected = orint.get()
    if middirected == 1:
        directed = True
        print_graph(input_list, directed)
    elif middirected == 2:
        directed = False
        print_graph(input_list, directed)
    else:
        tk.Label(win, text='Тип графа не выбран!', font=('Arial', 14)).pack()

def print_graph(edges, directed):
    tk.Label(win, text='Список смежности:', font=('Arial', 14)).pack()
    adjacency_list = graph_adjacency_list(edges, directed)
    for node, neighbors in adjacency_list.items():
        tk.Label(win, text=f"{node}: {neighbors}", font=('Arial', 10)).pack()
    tk.Label(win, text='Матрица смежности:', font=('Arial', 14)).pack()
    adjacency_matrix, nodes = graph_adjacency_matrix(edges, directed)
    for i, row in enumerate(adjacency_matrix):
        tk.Label(win, text=f"{nodes[i]}: {''.join(str(col) for col in row)}", font=('Arial', 10)).pack()
    tk.Label(win, text='Матрица инцидентности:', font=('Arial', 14)).pack()
    incidence_matrix, nodes, edges = graph_incidence_matrix(edges, directed)
    for i, row in enumerate(incidence_matrix):
        tk.Label(win, text=f"{nodes[i]}: {''.join(str(col) for col in row)}", font=('Arial', 10)).pack() 

def graph_adjacency_list(edges, directed):
    graph = {}
    for edge in edges:
        node1, node2 = edge[:2]
        if node1 not in graph:
            graph[node1] = []
        if node2 not in graph:
            graph[node2] = []
        graph[node1].append(node2)
        if not directed:
            graph[node2].append(node1)
    return graph

def graph_adjacency_matrix(edges, directed):
    nodes = list(set(itertools.chain(*edges)))
    nodes.sort()
    size = len(nodes)
    matrix = [[0] * size for _ in range(size)]
    for edge in edges:
        node1, node2 = edge[:2]
        index1, index2 = nodes.index(node1), nodes.index(node2)
        matrix[index1][index2] = 1
        if not directed:
            matrix[index2][index1] = 1
    return matrix, nodes

def graph_incidence_matrix(edges, directed):
    graph = graph_adjacency_list(edges, directed)
    nodes = list(graph.keys())
    nodes.sort()
    size = len(nodes)
    matrix = [[0] * len(edges) for _ in range(size)]
    for index, edge in enumerate(edges):
        node1, node2 = edge[:2]
        index1, index2 = nodes.index(node1), nodes.index(node2)
        matrix[index1][index] = 1
        if not directed:
            matrix[index2][index] = 1
    return matrix, nodes, edges

class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert(data, self.root)

    def _insert(self, data, node):
        if data < node.data:
            if node.left is None:
                node.left = Node(data)
            else:
                self._insert(data, node.left)
        else:
            if node.right is None:
                node.right = Node(data)
            else:
                self._insert(data, node.right)

    def find(self, data):
        if self.root:
            res = self._find(data, self.root)
            if res:
                return res.data
            else:
                return None
        else:
            return None

    def _find(self, data, node):
        if data == node.data:
            return node
        elif (data < node.data and node.left):
            return self._find(data, node.left)
        elif (data > node.data and node.right):
            return self._find(data, node.right)
        return None

    def delete(self, data):
        self.root = self._delete(self.root, data)

    def _delete(self, root, data):
        if root is None:
            return root
        if data < root.data:
            root.left = self._delete(root.left, data)
        elif(data > root.data):
            root.right = self._delete(root.right, data)
        else:
            if root.left is None:
                return root.right

            elif root.right is None:
                return root.left
            temp = self._minValueNode(root.right)
            root.data = temp.data
            root.right = self._delete(root.right, temp.data)
        return root

    def _minValueNode(self, root):
        current = root
        while(current.left is not None):
            current = current.left
        return current

    def traverse(self):
        if self.root is not None:
            self._traverse(self.root)

    def _traverse(self, node):
        if node is not None:
            self._traverse(node.left)
            tk.Label(win, text=node.data, font=('Arial', 10)).pack()
            self._traverse(node.right)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Бинарное дерево поиска")
        self.geometry("1600x900")
        self.tree = BinarySearchTree()
        self.label = tk.Label(self, text="Бинарное дерево поиска", font=('Arial', 20, 'bold'))
        self.label.pack()
        self.entry = tk.Entry(self, width=25)
        self.entry.pack()
        self.insert_button = tk.Button(self, text="ДОБАВИТЬ", command=self.insert)
        self.insert_button.pack()
        self.find_button = tk.Button(self, text="НАЙТИ", command=self.find)
        self.find_button.pack()
        self.delete_button = tk.Button(self, text="УДАЛИТЬ", command=self.delete)
        self.delete_button.pack()
        self.traverse_button = tk.Button(self, text="ОБХОД", command=self.traverse)
        self.traverse_button.pack()

    def insert(self):
        value = self.entry.get()
        self.tree.insert(int(value))
        messagebox.showinfo("Успех", f"Успешно добавлено: {value}")

    def find(self):
        value = self.entry.get()
        res = self.tree.find(int(value))
        if res:
            messagebox.showinfo("Успех", f"Найдено {value}")
        else:
            messagebox.showerror("Ошибка", f"{value} не найдено")

    def delete(self):
        value = self.entry.get()
        self.tree.delete(int(value))
        messagebox.showinfo("Успех", f"Успешное удаление {value}")

    def traverse(self):
        self.tree.traverse()
        messagebox.showinfo("Успех", "Успешный обход")

def create_list(message):
    list = dict(collections.Counter(message))
    list_sorted = sorted(iter(list.items()), key = lambda k_v:(k_v[1],k_v[0]),reverse=True)
    final_list = []
    for key,value in list_sorted:
        final_list.append([key,value,''])
    return final_list
    
def divide_list(list):
    if len(list) == 2:
        return [list[0]],[list[1]]
    else:
        n = 0
        for i in list:
            n+= i[1]
        x = 0
        distance = abs(2*x - n)
        j = 0
        for i in range(len(list)):
            x += list[i][1]
            if distance < abs(2*x - n):
                j = i
    return list[0:j+1], list[j+1:]

def label_list(list):
    list1,list2 = divide_list(list)
    for i in list1:
        i[2] += '0'
        c[i[0]] = i[2]
    for i in list2:
        i[2] += '1'
        c[i[0]] = i[2]
    if len(list1)==1 and len(list2)==1:
        return
    label_list(list2)
    return c

class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
    def children(self):
        return (self.left, self.right)
    def __str__(self):
        return '%s_%s' % (self.left, self.right)

def huffman_code_tree(node, binString=' '):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = {}
    d.update(huffman_code_tree(l, binString + '0'))
    d.update(huffman_code_tree(r, binString + '1'))
    return d

def make_tree(nodes):
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    return nodes[0][0]

def start_metod():
    global c
    clear()
    tk.Label(win, text='Введите сообщение для сжатия', font=('Arial', 14)).pack()
    tk.Entry(win, textvariable=voider, width=25).pack()
    tk.Button(win, text='ЗАПУСК', command=metod).pack()
    tk.Button(win, text='ВЕРНУТЬСЯ В МЕНЮ', fg='blue', command=main).pack()

def metod():
    message = voider.get()
    code = label_list(create_list(message))
    tk.Label(win, text='Код Шеннона-Фэно:', font=('Arial', 14)).pack()
    letter_binary = []
    for key, value in code.items():
        tk.Label(win, text=f'{key}  : {value}', font=('Arial', 10)).pack()
    letter_binary.append([key,value])
    string = message
    freq = Counter(string)
    nodes = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    node = make_tree(nodes)
    encoding = huffman_code_tree(node)
    tk.Label(win, text='Код Хаффмена:', font=('Arial', 14)).pack()
    for char in sorted(encoding):
        tk.Label(win, text=f'{char}  : {encoding[char]}', font=('Arial', 10)).pack()

def selalg():
    clear()
    tk.Label(win, text='Выберите алгоритм шифрования', font=('Arial', 14)).pack()
    tk.Button(win, text='LZ77', command=start_lz77).pack()
    tk.Button(win, text='LZ78', command=start_lz78).pack()
    tk.Button(win, text='LZSS', command=start_lzSS).pack()
    tk.Button(win, text='ВЕРНУТЬСЯ В МЕНЮ', fg='blue', command=main).pack()

def start_lz77():
    clear()
    tk.Label(win, text='Введите сообщение для сжатия: ', font=('Arial', 14)).pack()
    tk.Entry(win, textvariable=lz77_put, width=25).pack()
    tk.Button(win, text='ЗАПУСК', command=lz77).pack()
    tk.Button(win, text='ВЕРНУТЬСЯ В МЕНЮ', fg='blue', command=main).pack()

def lz77():
    data = lz77_put.get()
    compressed_data = lz77_compress(data)
    decompressed_data = lz77_decompress(compressed_data)
    tk.Label(win, text=f'Оригинальные данные: {data}', font=('Arial', 10)).pack()
    tk.Label(win, text=f'Сжатые данные: {compressed_data}', font=('Arial', 10)).pack()
    tk.Label(win, text=f'Распакованные данные: {decompressed_data}', font=('Arial', 10)).pack()

def lz77_compress(data, window_size=4096):
    compressed = []
    index = 0
    while index < len(data):
        best_offset = -1
        best_length = -1
        best_match = ''
        for length in range(1, min(len(data) - index, window_size)):
            substring = data[index:index + length]
            offset = data.rfind(substring, max(0, index - window_size), index)
            if offset != -1 and length > best_length:
                best_offset = index - offset
                best_length = length
                best_match = substring
        if best_match:
            compressed.append((best_offset, best_length, data[index + best_length]))
            index += best_length + 1
        else:
            compressed.append((0, 0, data[index]))
            index += 1
    return compressed

def lz77_decompress(compressed):
    decompressed = []
    for item in compressed:
        offset, length, next_char = item
        if length == 0:
            decompressed.append(next_char)
        else:
            start = len(decompressed) - offset
            substring = decompressed[start:start + length]
            decompressed.extend(substring)
            decompressed.append(next_char)
    return ''.join(decompressed)

def start_lz78():
    clear()
    tk.Label(win, text='Введите сообщение для сжатия: ', font=('Arial', 14)).pack()
    tk.Entry(win, textvariable=lz78_put, width=25).pack()
    tk.Button(win, text='ЗАПУСК', command=lz78).pack()
    tk.Button(win, text='ВЕРНУТЬСЯ В МЕНЮ', fg='blue', command=main).pack()

def lz78():
    data = lz78_put.get()
    compressed_data = lz78_compress(data)
    decompressed_data = lz78_decompress(compressed_data)
    tk.Label(win, text=f'Оригинальные данные: {data}', font=('Arial', 10)).pack()
    tk.Label(win, text=f'Сжатые данные: {compressed_data}', font=('Arial', 10)).pack()
    tk.Label(win, text=f'Распакованные данные: {decompressed_data}', font=('Arial', 10)).pack()
    
def lz78_compress(data):
    compressed = []
    dictionary = {}
    current_string = ""
    for char in data:
        current_string += char
        if current_string not in dictionary:
            index = len(dictionary) + 1
            dictionary[current_string] = index
            compressed.append((dictionary.get(current_string[:-1], 0), char))
            current_string = ""
    return compressed

def lz78_decompress(compressed):
    decompressed = []
    dictionary = {}
    for index, char in compressed:
        if index == 0:
            substring = char
        else:
            substring = dictionary[index] + char
        decompressed.append(substring)
        dictionary[len(dictionary) + 1] = substring
    return ''.join(decompressed)

def start_lzSS():
    clear()
    tk.Label(win, text='Введите сообщение для сжатия: ', font=('Arial', 14)).pack()
    tk.Entry(win, textvariable=lzSS_put, width=25).pack()
    tk.Button(win, text='ЗАПУСК', command=lzSS).pack()
    tk.Button(win, text='ВЕРНУТЬСЯ В МЕНЮ', fg='blue', command=main).pack()

def lzSS():
    data = lzSS_put.get()
    compressed_data = compress(data)
    decompressed_string = decompress(compressed_data)
    tk.Label(win, text=f'Оригинальные данные: {data}', font=('Arial', 10)).pack()
    tk.Label(win, text=f'Сжатые данные: {compressed_data}', font=('Arial', 10)).pack()
    tk.Label(win, text=f'Распакованные данные: {decompressed_string}', font=('Arial', 10)).pack()

def compress(input_string):
    window_size = 12
    lookahead_buffer_size = 4
    compressed_data = []
    pos = 0
    while pos < len(input_string):
        length = 0
        offset = 0
        for i in range(lookahead_buffer_size, 0, -1):
            if pos + i > len(input_string):
                continue
            current_window = input_string[pos:pos + i]
            prev_occurrence = input_string.rfind(current_window, 0, pos)
            if prev_occurrence != -1 and pos - prev_occurrence <= window_size:
                length = i
                offset = pos - prev_occurrence
                break
        if length > 0:
            encoded_pair = (length, offset)
            compressed_data.append(encoded_pair)
            pos += length
        else:
            encoded_pair = (0, input_string[pos])
            compressed_data.append(encoded_pair)
            pos += 1
    return compressed_data

def decompress(compressed_data):
    window_size = 12
    lookahead_buffer_size = 4
    decompressed_string = ""
    for encoded_pair in compressed_data:
        length, offset = encoded_pair
        if length > 0:
            start = len(decompressed_string) - offset
            end = start + length
            substring = decompressed_string[start:end]
            decompressed_string += substring
        else:
            decompressed_string += offset
    return decompressed_string

win = tk.Tk()
emblem = tk.PhotoImage(file='MAI.png') #Убрать если не нужна эмблема МАИ!
win.iconphoto(False, emblem)
win.geometry(f'1600x900')
win.title('Теория Информации МАИ')
vertex = tk.StringVar()
orint = tk.IntVar()
voider = tk.StringVar()
lz77_put = tk.StringVar()
lz78_put = tk.StringVar()
lzSS_put = tk.StringVar()
c = {}
main()
win.mainloop()
