const express = require('express');
const bodyParser = require('body-parser');
const { MongoClient } = require('mongodb');
const path = require('path');
const problemRoutes = require('./api/problemRoutes');
const signupRoutes = require('./api/signupRoutes');
const loginRoutes = require('./api/loginRoutes');
const logoutRoutes = require('./api/logoutRoutes');
const addProblemRoutes = require('./api/addProblemRoutes');
const updateCountRoutes = require('./api/updateCountRoutes');
const fetchCountRoutes = require('./api/fetchCountRoutes');
const searchRoutes = require('./api/searchRoutes');
const newSolveRoutes = require('./api/newSolveRoutes');
const recommendationRoutes = require('./api/recommendationRoutes');
const historyRoutes = require('./api/historyRoutes');
const removeSolveRoutes = require('./api/removeSolveRoutes');

const app = express();
const port = 3000;

app.use(express.static(path.join(__dirname, '')));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.json());

const uri = 'mongodb://localhost:27017';
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
app.locals.client = client;

async function connectToMongoDB() {
    try {
        await client.connect();
        console.log('Connected to MongoDB');
    } catch (error) {
        console.error('Error connecting to MongoDB:', error);
    }
}

connectToMongoDB();


app.use(problemRoutes);
app.use(signupRoutes);
app.use(loginRoutes);
app.use(logoutRoutes);
app.use(addProblemRoutes);
app.use(updateCountRoutes);
app.use(fetchCountRoutes);
app.use(searchRoutes);
app.use(newSolveRoutes);
app.use(recommendationRoutes);
app.use(historyRoutes);
app.use(removeSolveRoutes);




app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
