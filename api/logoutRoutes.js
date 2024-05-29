// logoutRoutes.js
const express = require('express');
const router = express.Router();

// Endpoint to handle user logout
router.post('/logout', async (req, res) => {
    const client = req.app.locals.client; // Access MongoDB client from app locals

    try {
        // Access the database and collection
        const db = client.db('repository');
        const currentUserCollection = db.collection('currentUser');

        // Delete all documents from the currentUser collection
        await currentUserCollection.deleteMany({});

        res.status(200).json({ message: 'Logout successful' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server Error' });
    }
});

module.exports = router;
