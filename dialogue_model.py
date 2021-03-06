
class DialogueModel:
    def __init__(self, dataset, dialogues, current_dialogue_index,  user_id):

        # Load data
        self.dataset = dataset

        # Set the user
        self.user_id = user_id

        # All dialogues
        self.dialogues = dialogues
        self.num_dialogues = len(self.dialogues)

        # Current dialogue
        self.current_dialogue_index = current_dialogue_index

        # Labelled and completed dialogue counts
        self.num_labelled = 0
        self.num_unlabelled = 0
        self.num_complete = 0
        self.num_incomplete = 0

        # Count labelled and unlabelled dialogues
        self.update_labelled_dialogue_counts()

    def __repr__(self):
        to_string = "Dataset: " + self.dataset + "\n"
        to_string += "User ID: " + self.user_id + "\n"
        to_string += "Num Dialogues: " + str(self.num_dialogues) + "\n"
        to_string += "Num Labelled: " + str(self.num_labelled) + "\n"
        to_string += "Num Unlabelled: " + str(self.num_unlabelled) + "\n"
        to_string += "Current Dialogue Index: " + str(self.current_dialogue_index)
        return to_string

    def get_current_dialogue(self):
        return self.dialogues[self.current_dialogue_index]

    def set_current_dialogue(self, index):
        self.current_dialogue_index = index
        return True

    def get_dialogue(self, dialogue_id):
        # Find the matching dialogue
        for dialogue in self.dialogues:
            if dialogue.dialogue_id == dialogue_id:
                return dialogue
            else:
                return False

    def set_dialogue(self, new_dialogue):
        # Find the matching dialogue
        for i, dialogue in enumerate(self.dialogues):
            if dialogue.dialogue_id == new_dialogue.dialogue_id:
                # Update dialogue with new data
                self.dialogues[i] = new_dialogue
                # Update dialogue states
                self.update_labelled_dialogue_counts()
                return True

    def update_labelled_dialogue_counts(self):

        # Reset labelled and completed counts
        self.num_labelled = 0
        self.num_unlabelled = 0
        self.num_complete = 0
        self.num_incomplete = 0

        # Update counts
        for dialogue in self.dialogues:

            # Labelled
            if dialogue.check_labels():
                self.num_labelled += 1
            else:
                self.num_unlabelled += 1
            # Completed
            if dialogue.is_complete:
                self.num_complete += 1
            else:
                self.num_incomplete += 1

    def inc_current_dialogue(self):

        # Increment dialogue index or wrap to beginning
        if self.current_dialogue_index + 1 < self.num_dialogues:
            self.current_dialogue_index += 1
        else:
            self.current_dialogue_index = 0

        return True

    def dec_current_dialogue(self):

        # Decrement dialogue index or wrap to end
        if self.current_dialogue_index - 1 < 0:
            self.current_dialogue_index = self.num_dialogues - 1
        else:
            self.current_dialogue_index -= 1

        return True


class Dialogue:

    def __init__(self, dialogue_id, utterances, num_utterances):
        self.dialogue_id = dialogue_id
        self.utterances = utterances
        self.num_utterances = num_utterances
        self.is_labelled = False
        self.is_complete = False
        self.time = 0
        self.questions = []
        self.check_labels()

    def __repr__(self):
        to_string = "Dialogue ID: " + self.dialogue_id + "\n"
        to_string += "Num Utterances: " + str(self.num_utterances) + "\n"
        to_string += "Labelled: " + str(self.is_labelled) + "\n"
        to_string += "Time: " + str(self.time) + "\n"
        # for utt in self.utterances:
        #     to_string += str(utt) + "\n"
        return to_string

    def set_is_labelled(self, value):
        if isinstance(value, bool):
            self.is_labelled = value
        else:
            print("Error! " + value + " is not a bool!")

    def set_is_complete(self, value):
        if isinstance(value, bool):
            self.is_complete = value
        else:
            print("Error! " + value + " is not a bool!")

    def set_time(self, value):
        if isinstance(value, int):
            self.time = value
        else:
            print("Error! " + value + " is not an int!")

    def set_questions(self, value):
        if isinstance(value, list):
            self.questions = value
        else:
            print("Error! " + value + " is not a list!")

    def check_labels(self):
        # Check if any utterances still have default labels
        for utt in self.utterances:
            if not utt.check_labels():
                self.is_labelled = False
                return self.is_labelled

        self.is_labelled = True
        return self.is_labelled


class Utterance:
    def __init__(self, text, speaker='', ap_label='AP-Label', da_label='DA-Label'):
        self.text = text
        self.speaker = speaker
        self.ap_label = ap_label
        self.da_label = da_label
        self.is_labelled = False
        self.ap_flag = False
        self.da_flag = False
        self.time = 0
        self.check_labels()

    def __repr__(self):
        return self.speaker + " " + self.text +\
                    " AP-Label: " + self.ap_label +\
                    " DA-Label: " + self.da_label +\
                    " Labelled: " + str(self.is_labelled)

    def set_ap_label(self, label):
        if isinstance(label, str):
            self.ap_label = label
            self.check_labels()
        else:
            print("Error! " + label + " is not a string!")

    def set_da_label(self, label):
        if isinstance(label, str):
            self.da_label = label
            self.check_labels()
        else:
            print("Error! " + label + " is not a string!")

    def set_is_labelled(self, value):
        if isinstance(value, bool):
            self.is_labelled = value
        else:
            print("Error! " + value + " is not a bool!")

    def set_ap_flag(self, value):
        if isinstance(value, bool):
            self.ap_flag = value
        else:
            print("Error! " + value + " is not a bool!")

    def set_da_flag(self, value):
        if isinstance(value, bool):
            self.da_flag = value
        else:
            print("Error! " + value + " is not a bool!")

    def set_time(self, value):
        if isinstance(value, int):
            self.time = value
        else:
            print("Error! " + value + " is not an int!")

    def check_labels(self):
        # Check if utterance still has default labels
        if self.ap_label == 'AP-Label' or self.da_label == 'DA-Label':
            self.is_labelled = False
            return self.is_labelled

        self.is_labelled = True
        return self.is_labelled
