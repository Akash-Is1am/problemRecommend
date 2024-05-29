const express = require('express');
const router = express.Router();
const { MongoClient } = require('mongodb');

router.post('/new-solve', async (req, res) => {
    const { problemId, problemLevel } = req.body;

    try {
        const client = req.app.locals.client;
        const db = client.db('repository');
        const currentUserCollection = db.collection('currentUser');

        // Fetch the user's email from the 'currentUser' collection
        const currentUser = await currentUserCollection.findOne({});
        const email = currentUser.email;

        // Check if the problem ID is not already present in the 'problems' field
        const userCollection = db.collection(email);
        const exist = await userCollection.findOne({ problems: problemId });
        if (!exist) {
            // Update the user's profile with the solved problem
            await userCollection.updateOne(
                {},
                {
                    $push: {
                        problems: problemId
                    },
                    $inc: {
                        [`${problemLevel.toLowerCase()}Count`]: 1
                    }
                }
            );

            res.status(200).send('Problem solved and profile updated successfully');
        } else {
            res.status(400).send('Problem already solved');
        }
    } catch (error) {
        console.error('Error updating profile with solved problem:', error);
        res.status(500).send('Error updating profile with solved problem');
    }
});

module.exports = router;
