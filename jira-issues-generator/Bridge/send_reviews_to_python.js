const spawn = require("child_process").spawn;

class SendReviewsToPython {
    constructor(pythonFilePath, userReviews, base64Authentication) {
        this.pythonProcess = spawn('python3', [pythonFilePath, JSON.stringify(userReviews), base64Authentication]);
    }

    listen() {
        this.pythonProcess.stdout.on('data', (data) => {
            // Do something with the data returned from python script
            console.log(data.toString());
        });

        this.pythonProcess.stderr.on('data', (data) => {
            console.log(data.toString());
        });

        this.pythonProcess.on('exit', (code) => {
            console.log('Process quit with code: ' + code);
            process.exit();
        });
    }
}

module.exports = {
    SendReviewsToPython
};
