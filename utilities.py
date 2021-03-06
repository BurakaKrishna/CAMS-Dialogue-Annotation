from random import shuffle
import traceback
import json
from dialogue_model import *


def load_json_data(path, file_name):
    try:
        with open(path + file_name + ".json") as file:
            data = json.load(file)

    except (IOError, ValueError):
        traceback.print_exc()
        return False

    return data


def save_json_data(path, file_name, data):
    try:
        with open(path + file_name + '.json', 'w+') as file:
            json.dump(data, file, sort_keys=False, indent=4, separators=(',', ': '))

    except (IOError, ValueError):
        traceback.print_exc()
        return False

    return True


def load_txt_data(path, file_name):
    try:
        with open(path + "/" + file_name + ".txt", "r") as file:
            # Read a line and strip newline char
            lines = [line.rstrip('\r\n') for line in file.readlines()]

    except (IOError, ValueError):
        traceback.print_exc()
        return False

    return lines


# Creates a dialogue model from the specified dialogue dataset file
def create_model(dialogue_data_path, data, user_id, user_data=False):

    # Create dialogue objects
    dialogues = dialogues_from_dict(data)

    # If we are not using existing user data add practice and shuffle
    if not user_data:
        practice_data = load_json_data(dialogue_data_path, "practice")
        practice_dialogue = dialogue_from_dict(practice_data)

        # Shuffle the actual dialogues and insert the practice at the start
        shuffle(dialogues)
        dialogues.insert(0, practice_dialogue)

    # If JSON is not valid or keys missing
    if not dialogues:
        print("Unable to load dialogues JSON data...")

    if 'current_dialogue_index' in data.keys():
        current_dialogue_index = data['current_dialogue_index']
    else:
        current_dialogue_index = 0

    # Create the dialogue model
    model = DialogueModel(data['dataset'], dialogues, current_dialogue_index, user_id)

    return model


def model_to_dict(model):

    # Convert model to dictionary
    model_dict = dict()
    model_dict['dataset'] = model.dataset
    model_dict['user_id'] = model.user_id
    model_dict['num_dialogues'] = model.num_dialogues
    model_dict['num_labelled'] = model.num_labelled
    model_dict['num_unlabelled'] = model.num_unlabelled
    model_dict['num_complete'] = model.num_complete
    model_dict['num_incomplete'] = model.num_incomplete
    model_dict['current_dialogue_index'] = model.current_dialogue_index
    model_dict['dialogues'] = dialogues_to_dict(model.dialogues)

    return model_dict


# Creates dialogue objects from dataset dictionary/json
def dialogues_from_dict(data):
    try:
        # Loop over the dialogues in the data
        dialogues = []
        for dialogue in data['dialogues']:

            # Create the dialogue
            tmp_dialogue = dialogue_from_dict(dialogue)

            # Add to dialogue list
            dialogues.append(tmp_dialogue)

    except KeyError:
        traceback.print_exc()
        return False

    return dialogues


# Creates a dialogue object and its utterances from dictionary/json
def dialogue_from_dict(dialogue):
    tmp_dialogue = None
    try:
        # Loop over the utterances in the dialogue
        utterances = []
        for utterance in dialogue['utterances']:

            # Create a new utterance
            tmp_utterance = Utterance(utterance['text'], utterance['speaker'])

            # Set utterance labels if not blank
            if utterance['ap_label'] is not "":
                tmp_utterance.set_ap_label(utterance['ap_label'])
            if utterance['da_label'] is not "":
                tmp_utterance.set_da_label(utterance['da_label'])

            # Set utterance flags if set
            if 'ap_flag' in utterance.keys():
                tmp_utterance.set_ap_flag(utterance['ap_flag'])
            if 'da_flag' in utterance.keys():
                tmp_utterance.set_da_flag(utterance['da_flag'])

            # Check if the labelled and time values are also set
            if 'is_labelled' in utterance.keys():
                tmp_utterance.set_is_labelled(utterance['is_labelled'])
            if 'time' in utterance.keys():
                tmp_utterance.set_time(utterance['time'])

            # Add to utterance list
            utterances.append(tmp_utterance)

        # Create a new dialogue with the utterances
        tmp_dialogue = Dialogue(dialogue['dialogue_id'], utterances, len(utterances))

        # Check if the labelled and time values are also set
        if 'is_labelled' in dialogue.keys():
            tmp_dialogue.set_is_labelled(dialogue['is_labelled'])
        if 'is_complete' in dialogue.keys():
            tmp_dialogue.set_is_complete(dialogue['is_complete'])
        if 'time' in dialogue.keys():
            tmp_dialogue.set_time(dialogue['time'])
        if 'questions' in dialogue.keys():
            tmp_dialogue.set_questions(dialogue['questions'])

    except KeyError:
        traceback.print_exc()

    # Check if the dialogue is labelled or not
    tmp_dialogue.check_labels()

    return tmp_dialogue


# Converts dialogue objects to a dictionary/list
def dialogues_to_dict(dialogues):
    dialogues_list = []

    # Loop over the dialogues and utterances
    for dialogue in dialogues:

        # Create a new dialogue with the utterances
        tmp_dialogue = dialogue_to_dict(dialogue)

        # Add to dialogue list
        dialogues_list.append(tmp_dialogue)

    return dialogues_list


# Converts a dialogue object and its utterances to a dictionary
def dialogue_to_dict(dialogue):
    dialogue_dict = dict()

    # Loop over utterances and add to dictionary
    utterances = []
    for utterance in dialogue.utterances:
        utt_dict = dict()

        # Add speaker, text and labels to utterance
        utt_dict['speaker'] = utterance.speaker
        utt_dict['text'] = utterance.text
        utt_dict['ap_label'] = utterance.ap_label
        utt_dict['da_label'] = utterance.da_label
        utt_dict['is_labelled'] = utterance.is_labelled
        utt_dict['time'] = utterance.time
        utt_dict['ap_flag'] = utterance.ap_flag
        utt_dict['da_flag'] = utterance.da_flag

        # Add to utterance list
        utterances.append(utt_dict)

    # Add id, number of utterances, utterances, is labelled and time to dialogue
    dialogue_dict['dialogue_id'] = dialogue.dialogue_id
    dialogue_dict['is_labelled'] = dialogue.is_labelled
    dialogue_dict['is_complete'] = dialogue.is_complete
    dialogue_dict['time'] = dialogue.time
    dialogue_dict['questions'] = dialogue.questions
    dialogue_dict['num_utterances'] = dialogue.num_utterances
    dialogue_dict['utterances'] = utterances

    return dialogue_dict
