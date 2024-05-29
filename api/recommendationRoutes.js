const express = require('express');
const router = express.Router();
const path = require('path');
const { execSync } = require('child_process');
const { MongoClient } = require('mongodb');
const fs = require('fs');

router.get('/recommend', async (req, res) => {
  try {
    const db = req.app.locals.client.db('repository');
    const currentUserCollection = db.collection('currentUser');

    const currentUser = await currentUserCollection.findOne({});
    const email = currentUser.email;

    const userCollection = db.collection(email);
    const solvedProblems = await userCollection.distinct('problems');
    
    const skillLevelResult = await userCollection.findOne({}, { projection: { problemSolvingRating: 1 } });
    const skillLevel = skillLevelResult ? skillLevelResult.problemSolvingRating : undefined;

    const problemCollection = db.collection('problems');
    const allProblems = await problemCollection.find({}).toArray();

    const skillLevelPath = path.join(__dirname, '..', 'recommendation', 'skillRating.json');
    fs.writeFileSync(skillLevelPath, JSON.stringify(skillLevel));
    
    const solvedProblemsPath = path.join(__dirname, '..', 'recommendation', 'solved_problems.json');
    fs.writeFileSync(solvedProblemsPath, JSON.stringify(solvedProblems));

    const allProblemsPath = path.join(__dirname, '..', 'recommendation', 'all_problems.json');
    fs.writeFileSync(allProblemsPath, JSON.stringify(allProblems));

    try {
      const pythonExecutablePath = 'C:\\Python312\\python.exe';
      const pythonScriptPath = path.join(
        'C:',
        'Users',
        'USER', // Replace 'USER' with your actual Windows username
        'Documents',
        'Project',
        'Repository',
        'recommendation',
        'recommend.py' // The script to execute
      );
      const output = execSync(`${pythonExecutablePath} ${pythonScriptPath}`, { encoding: 'utf-8' });
      // console.log(output);
    } catch (error) {
        console.error("Error executing Python script:", error);
    }

    const recommendationsPath = path.join(__dirname, '..', 'recommendation', 'recommendations.json');
    const recommendations = fs.readFileSync(recommendationsPath, 'utf8');
    res.send(recommendations);
  } catch (error) {
    console.error('Error fetching recommendations:', error);
    res.status(500).send('Internal Server Error');
  }
});

module.exports = router;
