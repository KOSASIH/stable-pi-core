// api/userDataAPI.js

class UserDataAPI {
    constructor(apiUrl) {
        this.apiUrl = apiUrl; // Base URL for the user data API
    }

    // Fetch user data by user ID
    async fetchUserData(userId) {
        try {
            const response = await fetch(`${this.apiUrl}/users/${userId}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const userData = await response.json();
            console.log("User data fetched successfully:", userData);
            return userData;
        } catch (error) {
            console.error("Error fetching user data:", error);
            throw error; // Rethrow the error for further handling
        }
    }

    // Update user profile
    async updateUserProfile(userId, profileData) {
        try {
            const response = await fetch(`${this.apiUrl}/users/${userId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(profileData),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const updatedUser = await response.json();
            console.log("User profile updated successfully:", updatedUser);
            return updatedUser;
        } catch (error) {
            console.error("Error updating user profile:", error);
            throw error; // Rethrow the error for further handling
        }
    }
}

// Example usage
const userAPI = new UserDataAPI('https://api.example.com'); // Replace with your actual API URL
userAPI.fetchUserData('12345').then(userData => {
    console.log("Fetched User Data:", userData);
}).catch(error => {
    console.error("Failed to fetch user data:", error);
});

// Example of updating user profile
const newProfileData = {
    name: "John Doe",
    email: "john.doe@example.com",
};
userAPI.updateUserProfile('12345', newProfileData).then(updatedUser => {
    console.log("Updated User Data:", updatedUser);
}).catch(error => {
    console.error("Failed to update user profile:", error);
});
