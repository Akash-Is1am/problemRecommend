const express = require('express');
const router = express.Router();

// Define route to fetch problems from MongoDB
router.get('/problems', async (req, res) => {
    try {
        const db = req.app.locals.client.db('repository'); // Access MongoDB client from app locals
        const problemCollection = db.collection('problems');
        const currentUserCollection = db.collection('currentUser');
        
        // Fetch the current user's email
        const currentUser = await currentUserCollection.findOne({});
        const email = currentUser.email;
        
        // Fetch the list of solved problems for the current user
        const userCollection = db.collection(email);
        const solvedProblems = await userCollection.distinct('problems');
        
        // Fetch all problems from the database
        const problems = await problemCollection.find({}).toArray();

        // Loop through each problem and check if it's solved for the current user
        problems.forEach(problem => {
            // Check if the current problem ID exists in the list of solved problems
            problem.solved = solvedProblems.includes(problem._id.toString());
        });

        res.json(problems);
    } catch (error) {
        console.error('Error fetching problems from MongoDB:', error);
        res.status(500).send('Internal Server Error');
    }
});

module.exports = router;
