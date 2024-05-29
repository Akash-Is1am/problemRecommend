const express = require('express');
const router = express.Router();
const { MongoClient } = require('mongodb');
const { ObjectId } = require('mongodb');

// Define route to fetch solved problems history from MongoDB
router.get('/history', async (req, res) => {
    try {
        const db = req.app.locals.client.db('repository'); // Access MongoDB client from app locals
        const currentUserCollection = db.collection('currentUser');

        // Fetch the current user's email
        const currentUser = await currentUserCollection.findOne({});
        const email = currentUser.email;

        // Fetch user's solved problems IDs
        const userCollection = db.collection(email);
        const solvedProblemIds = await userCollection.distinct('problems');
        const sanitizedIds = solvedProblemIds.map(id => new ObjectId(id));

        // Fetch details of solved problems from the problems collection
        const problemCollection = db.collection('problems');

        // Fetch details of solved problems from the problems collection
        const solvedProblems = await problemCollection.find({ _id: { $in: sanitizedIds } }).toArray();

        res.json(solvedProblems);
    } catch (error) {
        console.error('Error fetching solved problems history from MongoDB:', error);
        res.status(500).send('Internal Server Error');
    }
});

module.exports = router;
