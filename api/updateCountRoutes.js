// updateCountRoutes.js

const express = require('express');
const router = express.Router();
const { MongoClient } = require('mongodb');

router.post('/update-count', async (req, res) => {
    const { cppRating, problemSolvingRating, easyCount, mediumCount, hardCount } = req.body;

    try {
        const client = req.app.locals.client;
        const db = client.db('repository');
        const currentUserCollection = db.collection('currentUser');

        // Fetch the user's email from the 'currentUser' collection
        const currentUser = await currentUserCollection.findOne({});
        const email = currentUser.email;

        // Now you have the email and ratings, you can update the user's profile
        const userCollection = db.collection(email);

        await userCollection.updateOne(
            {},
            {
                $set: {
                    cppRating: parseInt(cppRating),
                    problemSolvingRating: parseInt(problemSolvingRating),
                    easyCount: parseInt(easyCount),
                    mediumCount: parseInt(mediumCount),
                    hardCount: parseInt(hardCount)
                }
            }
        );

        res.status(200).send('Ratings updated successfully');
    } catch (error) {
        console.error('Error updating ratings:', error);
        res.status(500).send('Error updating ratings');
    }
});

module.exports = router;
