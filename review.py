class Review:

    def __init__(self, reviewer, reviewed, review_data):
        self._reviewer = reviewer  # username of the person reviewing
        self._reviewed = reviewed  # username of the person reviewed
        self._review_data = review_data

    def get_reviewer(self):
        return self._reviewer

    def get_reviewed(self):
        return self._reviewed

    def get_review_data(self):
        return self._review_data


