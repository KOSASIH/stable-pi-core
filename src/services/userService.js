// src/services/userService.js

import AccessControl from '../core/accessControl';
import { generateQuantumToken, validateQuantumToken } from '../core/utils';

class UserService {
    constructor() {
        this.accessControl = new AccessControl();
    }

    // Register a new user with a specific role
    registerUser(username, role, privateKey) {
        try {
            // Check if the user already exists
            if (this.accessControl.users.has(username)) {
                throw new Error("User already exists.");
            }

            // Register the user and generate a quantum token
            const quantumToken = this.accessControl.registerUser(username, role, privateKey);
            console.log(`User ${username} registered successfully with role ${role}.`);
            return quantumToken;
        } catch (error) {
            this.handleError(error);
        }
    }

    // Authenticate a user and return their role
    authenticateUser(username, privateKey) {
        try {
            const role = this.accessControl.authenticateUser(username, privateKey);
            console.log(`User ${username} authenticated successfully with role ${role}.`);
            return role;
        } catch (error) {
            this.handleError(error);
        }
    }

    // Update user role
    updateUserRole(username, newRole, userRequestingRoleChange) {
        try {
            // Check if the user is authorized to change roles
            if (!this.accessControl.isAuthorized(userRequestingRoleChange, 'update')) {
                throw new Error("User is not authorized to update roles.");
            }

            const user = this.accessControl.users.get(username);
            if (!user) {
                throw new Error("User not found.");
            }

            user.role = newRole; // Update the user's role
            console.log(`User ${username}'s role updated to ${newRole}.`);
        } catch (error) {
            this.handleError(error);
        }
    }

    // Revoke user access
    revokeUserAccess(username, userRequestingRevocation) {
        try {
            // Check if the user is authorized to revoke access
            if (!this.accessControl.isAuthorized(userRequestingRevocation, 'revoke')) {
                throw new Error("User is not authorized to revoke access.");
            }

            this.accessControl.revokeAccess(username);
            console.log(`User ${username}'s access revoked successfully.`);
        } catch (error) {
            this.handleError(error);
        }
    }

    // Handle errors and log them
    handleError(error) {
        const timestamp = new Date().toISOString();
        console.error(`[${timestamp}] Error: ${error.message}`);
        throw new Error(error.message); // Rethrow the error for further handling
    }
}

export default UserService;
