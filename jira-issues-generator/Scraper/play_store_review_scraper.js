const gplay = require('google-play-scraper');

class PlayStoreReviewScraper {
    fetch(packageName, callback) {
        gplay.reviews({
            appId: packageName,
            page: 0,
            sort: gplay.sort.NEWEST
        }).then((reviews) => {
            // Get app meta-data from package name
            gplay.app({appId: packageName})
                .then((appData) => {
                    const currentAppVersion = appData['version'];
                    callback(reviews, currentAppVersion);
                }), (err) => {
                    console.log(err);
                    callback(null);
                }
        }, (err) => {
            console.log(err);
            callback(null);
        });
    }
}

module.exports = {
    PlayStoreReviewScraper
};
