class AppIdInputReceiver {
    promptUserToFillAppId(callback) {
        const readlineSync = require('readline-sync');

        // platform
        const platform = readlineSync.question('Please select platform that you want. If you want to exit, type others key then press enter.\n1. iOS\n2. Android\n');

        // app id
        var appIdQuestion;
        if (platform == '1') {
            appIdQuestion = 'Please input your Bundle ID.\n';
        } else if (platform == '2') {
            appIdQuestion = 'Please input your Package Name.\n'
        } else {
            console.log('program exit');
            process.exit();
        }
        const appId = readlineSync.question(appIdQuestion);

        const projectId = readlineSync.question('Please input your project id.\n');
        const bugIssueId = readlineSync.question('Please input your bug issue id.\n');
        const featureIssueId = readlineSync.question('Please input your feature issue id.\n');
        const iosComponentId = readlineSync.question('Please input your iOS component id.\n');
        const androidComponentId = readlineSync.question('Please input your Android component id.\n');

        // jira username
        const jiraUsername = readlineSync.question('Please input your Jira username.\n');

        // jira api token
        const jiraPassword = readlineSync.question('Please input your Jira API token.\n', {
            hideEchoBack: true
        });

        // process base64 value for authorization.
        let buff = Buffer.from(jiraUsername + ':' + jiraPassword);
        let base64data = buff.toString('base64')

        callback(appId, platform, base64data);
    }
}

module.exports = {
    AppIdInputReceiver
};
