"""
Data Manager Module

This module manages data listings in the Orbital Data Marketplace, allowing
users to add, update, retrieve, and remove data listings.
"""

class DataManager:
    def __init__(self):
        self.listings = {}  # Dictionary to hold data listings
        self.next_id = 1    # ID counter for listings

    def add_listing(self, seller, data_description, price):
        """
        Add a new data listing.

        :param seller: Address of the seller
        :param data_description: Description of the data
        :param price: Price of the data
        :return: Listing ID of the new listing
        """
        listing_id = self.next_id
        self.listings[listing_id] = {
            'seller': seller,
            'data_description': data_description,
            'price': price,
            'is_sold': False
        }
        self.next_id += 1
        return listing_id

    def update_listing(self, listing_id, new_description, new_price):
        """
        Update an existing data listing.

        :param listing_id: ID of the listing to update
        :param new_description: New description for the data
        :param new_price: New price for the data
        """
        if listing_id in self.listings:
            self.listings[listing_id]['data_description'] = new_description
            self.listings[listing_id]['price'] = new_price
        else:
            raise ValueError("Listing ID not found.")

    def get_listing(self, listing_id):
        """
        Retrieve a data listing by ID.

        :param listing_id: ID of the listing to retrieve
        :return: Listing details
        """
        return self.listings.get(listing_id, "Listing ID not found.")

    def remove_listing(self, listing_id):
        """
        Remove a data listing.

        :param listing_id: ID of the listing to remove
        """
        if listing_id in self.listings:
            del self.listings[listing_id]
        else:
            raise ValueError("Listing ID not found.")

    def get_all_listings(self):
        """
        Retrieve all data listings.

        :return: List of all listings
        """
        return self.listings
