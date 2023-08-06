import maglev
import englishauction

class EnglishAuction:
	"""
	An Auction Library
	Timed auction starting at a low price and increasing until no more bids are made.
	Also supports reserve price and automatic bidding.
	"""
	def __init__(self):
		bus = maglev.maglev_MagLev.getInstance("default")
		lib = englishauction.englishauction_EnglishAuction(bus)

	def Create(self, start: string, end: string, startingPrice: number, reservePrice: number, priceIncrement: number) -> string:
		"""		Create a new auction
		Args:
			start (string):start time of auction
			end (string):end time of auction
			startingPrice (number):starting price of auction
			reservePrice (number):reserve price for the auction (0 = none)
			priceIncrement (number):price increments for bids in the auction
		Returns:
			auctionId
		"""
		bus = maglev.maglev_MagLev.getInstance("default")
		args = [start, end, startingPrice, reservePrice, priceIncrement]
		ret = bus.call('EnglishAuction.Create', args);
		return ret;

	def GetStart(self, auctionId: string) -> number:
		"""		Get the start of an auction
		Will return a timestamp in milliseconds
		Args:
			auctionId (string):auction id
		Returns:
			start of auction
		"""
		bus = maglev.maglev_MagLev.getInstance("default")
		args = [auctionId]
		ret = bus.call('EnglishAuction.GetStart', args);
		return ret;

	def GetEnd(self, auctionId: string) -> bool:
		"""		Check if auction has ended
		Args:
			auctionId (string):auction id
		Returns:
			true if auction has ended, false otherwise
		"""
		bus = maglev.maglev_MagLev.getInstance("default")
		args = [auctionId]
		ret = bus.call('EnglishAuction.GetEnd', args);
		return ret;

	def HasStarted(self, auctionId: string) -> bool:
		"""		Check if an auction has started yet
		Args:
			auctionId (string):auction id
		Returns:
			true if auction started, false otherwise
		"""
		bus = maglev.maglev_MagLev.getInstance("default")
		args = [auctionId]
		ret = bus.call('EnglishAuction.HasStarted', args);
		return ret;

	def Bid(self, auctionId: string, userId: string, price: number):
		"""		Create a bid in an auction
		Args:
			auctionId (string):auction id
			userId (string):user id
			price (number):price bud
		"""
		bus = maglev.maglev_MagLev.getInstance("default")
		args = [auctionId, userId, price]
		bus.call('EnglishAuction.Bid', args);

	def GetHighestBidder(self, auctionId: string) -> mixed:
		"""		Get the highest bidder in an auction
		Args:
			auctionId (string):auction id
		Returns:
			
		"""
		bus = maglev.maglev_MagLev.getInstance("default")
		args = [auctionId]
		ret = bus.call('EnglishAuction.GetHighestBidder', args);
		return ret;

	def GetHighestBids(self, auctionId: string, numBids: number) -> array:
		"""		Get the highest bids in an auction
		Args:
			auctionId (string):auction id
			numBids (number):max number of highest bids to return
		Returns:
			Highest bids for the specified auction
		"""
		bus = maglev.maglev_MagLev.getInstance("default")
		args = [auctionId, numBids]
		ret = bus.call('EnglishAuction.GetHighestBids', args);
		return ret;

	def GetNumberOfBids(self, auctionId: string) -> number:
		"""		Get the number of bids in an auction
		Args:
			auctionId (string):auction id
		Returns:
			Number of bids placed in the specified auction
		"""
		bus = maglev.maglev_MagLev.getInstance("default")
		args = [auctionId]
		ret = bus.call('EnglishAuction.GetNumberOfBids', args);
		return ret;

	def GetPriceIncrement(self, auctionId: string) -> number:
		"""		Get the price increment for the specified auction
		Args:
			auctionId (string):auction id
		Returns:
			Price increment
		"""
		bus = maglev.maglev_MagLev.getInstance("default")
		args = [auctionId]
		ret = bus.call('EnglishAuction.GetPriceIncrement', args);
		return ret;

	def GetReservePrice(self, auctionId: string) -> number:
		"""		Get the reserve price for the specified auction
		Args:
			auctionId (string):auction id
		Returns:
			Reserve price
		"""
		bus = maglev.maglev_MagLev.getInstance("default")
		args = [auctionId]
		ret = bus.call('EnglishAuction.GetReservePrice', args);
		return ret;

	def GetStartingPrice(self, auctionId: string) -> number:
		"""		Get the starting price for the specified auction
		Args:
			auctionId (string):auction id
		Returns:
			Starting price
		"""
		bus = maglev.maglev_MagLev.getInstance("default")
		args = [auctionId]
		ret = bus.call('EnglishAuction.GetStartingPrice', args);
		return ret;

	def CalcTimeRemaining(self, auctionId: string, now: number) -> number:
		"""		Get the time remaining for the specified auction
		Args:
			auctionId (string):auction id
			now (number):current unix timestamp
		Returns:
			Time remaining in seconds
		"""
		bus = maglev.maglev_MagLev.getInstance("default")
		args = [auctionId, now]
		ret = bus.call('EnglishAuction.CalcTimeRemaining', args);
		return ret;

	def CalcMinimumBid(self, auctionId: string) -> number:
		"""		Get the minimum next bid for the specified auction
		Args:
			auctionId (string):auction id
		Returns:
			Minimum bid price
		"""
		bus = maglev.maglev_MagLev.getInstance("default")
		args = [auctionId]
		ret = bus.call('EnglishAuction.CalcMinimumBid', args);
		return ret;

	def GetAuctionsEnding(self, endfrom: number, endto: number, page: number, perpage: number, sort: string, asc: bool) -> array:
		"""		Get a list of auctions based on their end time
		Args:
			endfrom (number):end from
			endto (number):end to
			page (number):
			perpage (number):number of auctions per page
			sort (string):field to sort by
			asc (bool):ascending (true) or descending (false)
		Returns:
			List of auctions ending in the specified period
		"""
		bus = maglev.maglev_MagLev.getInstance("default")
		args = [endfrom, endto, page, perpage, sort, asc]
		ret = bus.call('EnglishAuction.GetAuctionsEnding', args);
		return ret;

	def GetAuctionsStarting(self, startfrom: number, startto: number, page: number, perpage: number, sort: string, asc: bool) -> array:
		"""		Get a list of auctions based on their start time
		Args:
			startfrom (number):start from
			startto (number):start to
			page (number):
			perpage (number):number of auctions per page
			sort (string):field to sort by
			asc (bool):ascending (true) or descending (false)
		Returns:
			List of auctions starting in the specified period
		"""
		bus = maglev.maglev_MagLev.getInstance("default")
		args = [startfrom, startto, page, perpage, sort, asc]
		ret = bus.call('EnglishAuction.GetAuctionsStarting', args);
		return ret;

	def GetOpenAuctions(self, page: number, perpage: number, sort: string, asc: bool) -> array:
		"""		Get a list of currently running auctions
		Args:
			page (number):
			perpage (number):number of auctions per page
			sort (string):field to sort by
			asc (bool):ascending (true) or descending (false)
		Returns:
			List of open auctions
		"""
		bus = maglev.maglev_MagLev.getInstance("default")
		args = [page, perpage, sort, asc]
		ret = bus.call('EnglishAuction.GetOpenAuctions', args);
		return ret;



