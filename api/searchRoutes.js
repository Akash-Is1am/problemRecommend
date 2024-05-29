// searchRoutes.js
const express = require('express');
const router = express.Router();

router.get('/search', async (req, res) => {
    try {
        const client = req.app.locals.client;
        const db = client.db('repository');
        const problemCollection = db.collection('problems');
        const currentUserCollection = db.collection('currentUser');
        
        // Fetch the current user's email
        const currentUser = await currentUserCollection.findOne({});
        const email = currentUser.email;
        
        // Fetch the list of solved problems for the current user
        const userCollection = db.collection(email);
        const solvedProblems = await userCollection.distinct('problems');

        const searchQuery = req.query.search; // Get the search query from the request URL

        // Perform the search in the 'problems' collection based on the 'tags' field
        const searchResults = await problemCollection.find({ tags: searchQuery }).toArray();

        // Loop through search results and add solved flag for each problem
        searchResults.forEach(problem => {
            // Check if the current problem ID exists in the list of solved problems
            problem.solved = solvedProblems.includes(problem._id.toString());
        });

        res.json(searchResults); // Send the search results with solved flag as JSON response
    } catch (error) {
        console.error('Error searching problems:', error);
        res.status(500).send('Error searching problems');
    }
});

module.exports = router;
