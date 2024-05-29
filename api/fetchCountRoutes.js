// fetchCountRoutes.js

const express = require('express');
const router = express.Router();
const { MongoClient } = require('mongodb');

router.get('/fetch-count', async (req, res) => {

    try {
        const client = req.app.locals.client;
        const db = client.db('repository');
        const currentUserCollection = db.collection('currentUser');

        // Fetch the user's email from the 'currentUser' collection
        const currentUser = await currentUserCollection.findOne({});
        const email = currentUser.email;

        const userCollection = db.collection(email);
        const userDocument = await userCollection.findOne({});

        const data = {
            cppRating: userDocument.cppRating,
            problemSolvingRating: userDocument.problemSolvingRating,
            easyCount: userDocument.easyCount,
            mediumCount: userDocument.mediumCount,
            hardCount: userDocument.hardCount
        };

        res.json(data);

    } catch (error) {
        console.error('Error fetching ratings:', error);
        res.status(500).send('Error fetching ratings');
    }
});

module.exports = router;
