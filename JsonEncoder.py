#!/usr/bin/env python3
import json
import sys
import argparse
from pathlib import Path


class Node:
    def __init__(self, node_id, node_labels, level=0):
        self.id = node_id
        self.labels = node_labels
        self.level = level
        self.children = []

    def add_child(self, child):
        self.children.append(child)


class ClumpinessTreeBuilder:

    def __init__(self, input_json_file):
        self.json_object = self.__class__.load_json(input_json_file)
        self.root = None
        self.node_id = 0
        self.metadata = None
        self.output_stream = sys.stdout

    def builder_print(self, *objects):
        print(*objects, sep=' ', end='\n', file=self.output_stream, flush=False)

    @staticmethod
    def load_json(file):
        with open(file) as f:
            return json.load(f)

    def build_tree(self, metadata):
        self.metadata = metadata
        self.root = self.traverse(self.json_object['tree'])

    def traverse(self, json_obj):
        labels = []
        for seq, prop in json_obj['data']['seq_ids'].items():
            prop_metadata = prop['metadata'][self.metadata]
            if type(prop_metadata) == list:
                labels.extend(prop_metadata)
            else:
                labels.append(prop_metadata)
        node = Node(self.node_id, labels)
        self.node_id += 1
        for child in json_obj['children']:
            node.add_child(self.traverse(child))
        return node

    def dump_tree(self, output_stream=sys.stdout):
        self.output_stream = output_stream
        self.builder_print("[")
        self.dump(self.root, 1)
        self.builder_print("]")

    def dump(self, node, indent):
        indentation = '\t' * indent
        self.builder_print(indentation + "{")
        if len(node.labels) == 0:
            self.builder_print(indentation + "\t\"nodeID\": \"ID\",\n" + indentation + "\t\"nodeLabels\": []")
        else:
            self.builder_print(indentation + "\t\"nodeID\": \"ID\",\n" + indentation + "\t\"nodeLabels\": [")
            temp_str = ""
            for label in node.labels:
                if len(temp_str) > 0:
                    self.builder_print(temp_str)
                temp_str = indentation + "\t\t\"" + label + "\","
            self.builder_print(temp_str[:-1] + "\n" + indentation + "\t]")
        self.builder_print(indentation + "},")
        if len(node.children) == 0:
            self.builder_print(indentation + "[]")
            return
        self.builder_print(indentation + "[")
        temp_str = ""
        for child in node.children:
            if len(temp_str) > 0:
                self.builder_print(temp_str)
            self.builder_print(indentation + "\t[")
            self.dump(child, indent + 2)
            temp_str = indentation + "\t],"
        self.builder_print(temp_str[:-1])
        self.builder_print(indentation + "]")
        return

# Clumpiness/JsonEncoder.py Clumpiness/test/original_final_1.JSON tissue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts the new json format to the old json format used in the '
                                                 'clumpiness application.')
    parser.add_argument('-i', '--input_file', dest='input_json', type=str, required=True,
                        help='path to the input json file in the new format')
    parser.add_argument('-m', '--metadata', dest='metadata', required=True,
                        help='name of the metadata to extract')
    parser.add_argument('-o', '--output_file', dest='output_json', type=str,
                        help='path to the file to dump the generated json file in the old format '
                             '(default: standard output)')

    args = parser.parse_args()
    input_json = args.input_json
    metadata = args.metadata
    builder = ClumpinessTreeBuilder(input_json)
    builder.build_tree(metadata)
    if args.output_json:
        with open(Path(args.output_json), 'w') as f:
            builder.dump_tree(f)
    else:
        builder.dump_tree()
