const mysql = require('mysql');
const fs = require('fs');

const connection = mysql.createConnection({
    host     : 'localhost',
    database : 'user_reviews',
    user     : 'root',
    password : 'root',
    socketPath: '/Applications/MAMP/tmp/mysql/mysql.sock'
});

connection.connect(function(err) {
    if (err) {
        console.error('Error connecting: ' + err.stack);
        return ;
    }

    console.log('Connected as id ' + connection.threadId);
});

const file_names = [
    'Bug_Report_Data',
    'Bug_Report_Data_Test',
    'Bug_Report_Data_Train',
    'Feature_OR_Improvment_Request_Data',
    'Feature_OR_Improvment_Request_Data_Test',
    'Feature_OR_Improvment_Request_Data_Train',
    'Not_Bug_Report_Data',
    'Not_Bug_Report_Data_Test',
    'Not_Bug_Report_Data_Train',
    'Not_Feature_OR_Improvment_Request_Data',
    'Not_Feature_OR_Improvment_Request_Data_Test',
    'Not_Feature_OR_Improvment_Request_Data_Train',
    'Not_Rating_Data',
    'Not_Rating_Data_Test',
    'Not_Rating_Data_Train',
    'Not_UserExperience_Data',
    'Not_UserExperience_Data_Test',
    'Not_UserExperience_Data_Train',
    'Rating_Data',
    'Rating_Data_Test',
    'Rating_Data_Train',
    'UserExperience_Data',
    'UserExperience_Data_Test',
    'UserExperience_Data_Train'
];

for (index in file_names) {
    const file_name = file_names[index];

    connection.query('SELECT * FROM ' + file_name, function(error, results, fields) {
        if (error) {
            throw error;
        }
    
        fs.writeFile('json_data/' + file_name + '.json', JSON.stringify(results), function(err) {
            if (err) {
                throw err;
            }
            console.log(file_name + ' has been saved!');

            if (file_name == 'UserExperience_Data_Train') {
                connection.end();
            }
        });
    });
}