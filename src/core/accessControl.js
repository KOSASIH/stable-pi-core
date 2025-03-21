// src/core/accessControl.js

import { generateQuantumToken, validateQuantumToken } from './utils';

class AccessControl {
    constructor() {
        this.users = new Map(); // Store users with their roles and permissions
    }

    // Method to register a new user with a specific role
    registerUser(username, role, privateKey) {
        if (this.users.has(username)) {
            throw new Error("User already exists.");
        }
        const quantumToken = generateQuantumToken(username, role, privateKey);
        this.users.set(username, { role, quantumToken });
        return quantumToken;
    }

    // Method to validate user credentials and generate a quantum token
    authenticateUser(username, privateKey) {
        const user = this.users.get(username);
        if (!user) {
            throw new Error("User not found.");
        }
        const isValid = validateQuantumToken(user.quantumToken, privateKey);
        if (!isValid) {
            throw new Error("Invalid credentials.");
        }
        return user.role; // Return the user's role upon successful authentication
    }

    // Method to check if a user is authorized to perform a specific action
    isAuthorized(user, action) {
        const permissions = this.getPermissions(user.role);
        return permissions.includes(action);
    }

    // Method to define permissions based on user roles
    getPermissions(role) {
        const rolePermissions = {
            admin: ['create', 'read', 'update', 'delete', 'rewind'],
            user: ['read', 'create'],
            guest: ['read'],
        };
        return rolePermissions[role] || [];
    }

    // Method to revoke access for a user
    revokeAccess(username) {
        if (!this.users.has(username)) {
            throw new Error("User not found.");
        }
        this.users.delete(username);
    }

    // Method to log access attempts (for auditing purposes)
    logAccessAttempt(username, action, success) {
        const timestamp = new Date().toISOString();
        console.log(`[${timestamp}] Access attempt by ${username} for action "${action}": ${success ? 'SUCCESS' : 'FAILURE'}`);
    }
}

export default AccessControl;
