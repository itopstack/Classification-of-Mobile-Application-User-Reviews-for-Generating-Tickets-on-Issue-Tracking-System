const fs = require('fs');

fs.readFile('text_similarity_test.json', 'utf8', function (err, data) {
    if (err) {
        throw err;
    }

    var objs = JSON.parse(data);
    for (i in objs) {
        var obj = objs[i];
        obj.similarity_id = "T" + i;
    }

    fs.writeFile('./text_similarity_test.json', JSON.stringify(objs) , 'utf-8', (err) => {
        if (err) {
            console.log(err);
            return ;
        }

        console.log('Write file successfully!');
    });
});