// addProblemRoutes.js

const express = require('express');
const router = express.Router();

// Route to handle form submission for adding a new problem
router.post('/add', async (req, res) => {
    const client = req.app.locals.client; // Access MongoDB client from app locals
    const db = client.db('repository'); // Access the 'repository' database
    const problemsCollection = db.collection('problems'); // Access the 'problems' collection
    // Extract form data
    const { name, platforms, level, link, tags } = req.body;

    try {
        // Insert the new problem into the 'problems' collection
        const result = await problemsCollection.insertOne({
            name,
            tags: tags.split(','), // Assuming tags is a comma-separated string
            platforms: platforms.split(','), // Assuming platforms is a comma-separated string
            level,
            link
        });

        // Check if insertion was successful
        if (result.acknowledged) {
            console.log('Problem added successfully');
            // Send success response
            res.status(200).send('Problem added successfully');
        } else {
            console.error('Failed to add problem: No document was inserted');
            res.status(500).send('Failed to add problem');
        }
    } catch (error) {
        console.error('Error adding problem:', error);
        res.status(500).send('Error adding problem');
    }
});

module.exports = router;
