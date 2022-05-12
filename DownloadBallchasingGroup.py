import ballchasing

replayGroupLink = "https://ballchasing.com/group/eurc-2022-xfproo3jmu"


class BallchasingConnection():
	def __init__(self) -> None:
		self.apiToken = "otD1YFTrYz5sUy7GfZBW9mMNTB66QTLnQcqrpeIS"
		self.api = ballchasing.Api(self.apiToken, print_on_rate_limit = True)
	def GetGroup(self, group):
		print(self.api.download_group)



api = ballchasing.Api("otD1YFTrYz5sUy7GfZBW9mMNTB66QTLnQcqrpeIS")
api.download_group("eurc-2022-xfproo3jmu", r"E:\Rocket League Replays\EURC Replay Group", unrevise = False)