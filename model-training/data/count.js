const fs = require('fs');
const paths = ['./all.json', 
                './Bug.json', 
                './Feature.json', 
                './Rating.json', 
                './UserExperience.json'];

for (i in paths) {
    const path = paths[i];

    fs.readFile(path, (err, data) => {  
        if (err) {
            console.log(err);
            return ;
        }
        const jsons = JSON.parse(data);
        console.log(path + ' = ' + jsons.length + ' objects.');
    });
}

