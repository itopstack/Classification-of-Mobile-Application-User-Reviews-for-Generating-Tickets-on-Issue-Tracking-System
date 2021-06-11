const store = require('app-store-scraper');

class AppStoreReviewScraper {
    fetch(bundleId, callback) {
        store.reviews({
            appId: bundleId,
            sort: store.sort.RECENT,
            page: 1
        })
        .then((reviews) => {
            callback(reviews)
        })
        .catch((err) => {
            console.log(err);
            callback(null);
        });
    }
}

module.exports = {
    AppStoreReviewScraper
};
