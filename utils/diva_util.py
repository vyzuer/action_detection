import yaml
import os
import numpy as np
import cv2

annotations_mapping = {0: 'activities', 1: 'geom', 2: 'regions', 3:'types'}


def get_annotation_files(annotations_dir, annotation_key):
    files = []
    cameras = os.listdir(annotations_dir)
    for camera in cameras:
        if os.path.isdir(os.path.join(annotations_dir, camera)):
            videos = os.listdir(os.path.join(annotations_dir, camera))
            for video in videos:
                annotation_files = os.listdir(os.path.join(annotations_dir, camera, video))
                for annotation_file in annotation_files:
                    annotation_type = annotation_file.split('.')[1]
                    if annotation_type == annotations_mapping[annotation_key]:
                        files.append(os.path.join(annotations_dir, camera, video, annotation_file))
    return files


def get_actors_count():
    actors_count = 0
    annotation_files = get_annotation_files(3)
    for annotation_file in annotation_files:
        annotations = yaml.load(open(annotation_file, 'r'))
        for annotation in annotations:
            if isinstance(annotation, dict) and 'meta' in annotation.keys():
                meta_annotation = annotation['meta']
                if meta_annotation is not None:
                    splits = meta_annotation.split(" ")
                    if splits[-1] == 'instances':
                        count = splits[-2]
                        if count.isdigit():
                            actors_count += int(count)
                        else:
                            print(meta_annotation)
    return actors_count


def get_actor_bboxes(annotations_dir, cam_id, video_id):
    geom_annotation_file = os.path.join(annotations_dir, cam_id, video_id, video_id + '.geom.yml')
    annotations = yaml.load(open(geom_annotation_file, 'r'))
    output = {}
    for annotation in annotations:
        if 'meta' not in annotation.keys():
            actor_id = annotation['geom']['id1']
            frame_number = annotation['geom']['ts0']
            bbox = annotation['geom']['g0']
            bbox = [int(value) for value in bbox.split(" ")]
            if actor_id in output:
                output[actor_id]['frames'].append(frame_number)
                output[actor_id]['bboxes'].append(bbox)
            else:
                output[actor_id] = {}
                output[actor_id]['frames'] = []
                output[actor_id]['bboxes'] = []
                output[actor_id]['frames'].append(frame_number)
                output[actor_id]['bboxes'].append(bbox)
    return output


def get_bboxes_for_actor(annotations_dir, cam_id, video_id, actor_id):
    geom_annotation_file = os.path.join(annotations_dir, cam_id, video_id, video_id + '.geom.yml')
    annotations = yaml.load(open(geom_annotation_file, 'r'))
    output = {}
    output['frames'] = []
    output['bboxes'] = []
    for annotation in annotations:
        if 'meta' not in annotation.keys():
            if actor_id == annotation['geom']['id1']:
                frame_number = annotation['geom']['ts0']
                bbox = annotation['geom']['g0']
                bbox = [int(value) for value in bbox.split(" ")]
                output['frames'].append(frame_number)
                output['bboxes'].append(bbox)
    return output


def get_bboxes_for_actors(annotations_dir, cam_id, video_id, actor_ids):
    geom_annotation_file = os.path.join(annotations_dir, cam_id, video_id, video_id + '.geom.yml')
    annotations = yaml.load(open(geom_annotation_file, 'r'))
    output = {}
    for annotation in annotations:
        if 'meta' not in annotation.keys():
            actor_id = annotation['geom']['id1']
            if actor_id in actor_ids:
                frame_number = annotation['geom']['ts0']
                bbox = annotation['geom']['g0']
                bbox = [int(value) for value in bbox.split(" ")]
                if actor_id in output:
                    output[actor_id]['frames'].append(frame_number)
                    output[actor_id]['bboxes'].append(bbox)
                else:
                    output[actor_id] = {}
                    output[actor_id]['frames'] = []
                    output[actor_id]['bboxes'] = []
                    output[actor_id]['frames'].append(frame_number)
                    output[actor_id]['bboxes'].append(bbox)
        return output


def get_actor_ids(annotations_dir, cam_id, video_id):
    geom_annotation_file = os.path.join(annotations_dir, cam_id, video_id, video_id + '.types.yml')
    annotations = yaml.load(open(geom_annotation_file, 'r'))
    actor_ids = []
    for annotation in annotations:
        if 'meta' not in annotation.keys():
            actor_id = annotation['types']['id1']
            actor_ids.append(actor_id)
    return actor_ids


def get_actor_ids_of_type(annotations_dir, cam_id, video_id, actor_type):
    geom_annotation_file = os.path.join(annotations_dir, cam_id, video_id, video_id + '.types.yml')
    annotations = yaml.load(open(geom_annotation_file, 'r'))
    actor_ids = []
    for annotation in annotations:
        if 'meta' not in annotation.keys():
            actor_id = annotation['types']['id1']
            obj_type = annotation['types']['obj_type']
            if obj_type == actor_type:
                actor_ids.append(actor_id)
    return actor_ids
