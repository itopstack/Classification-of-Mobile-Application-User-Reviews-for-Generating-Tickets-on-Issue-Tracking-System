const { AppIdInputReceiver } = require('./UserInput/app_id_input_receiver');
const { AppStoreReviewScraper } = require('./Scraper/app_store_review_scraper');
const { PlayStoreReviewScraper } = require('./Scraper/play_store_review_scraper');
const { SendReviewsToPython } = require('./Bridge/send_reviews_to_python');

function connectToPython(reviews) {
    if (reviews == null || reviews.length == 0) {
        console.log('program exit');
        process.exit();
    }

    const bridge = new SendReviewsToPython('./main.py', reviews, base64Authentication);
    bridge.listen();
}

var base64Authentication;
var receiverCallback = (appId, platform, base64Data) => {
    base64Authentication = base64Data;

    if (platform == '1') { // iOS
        // e.g. com.facebook.Facebook
        const appStoreScraper = new AppStoreReviewScraper();
        appStoreScraper.fetch(appId, appStoreScraperCallback);

    } else if (platform == '2') { // Android
        // e.g. com.facebook.katana
        const playStoreScraper = new PlayStoreReviewScraper();
        playStoreScraper.fetch(appId, playStoreScraperCallback);
    }
}

const appStoreScraperCallback = (reviews) => {
    reviews.forEach(review => {
        review['platform'] = 'iOS';
    });

    connectToPython(reviews)
}

const playStoreScraperCallback = (reviews, currentAppVersion) => {
    reviews.forEach(review => {
        review['version'] = currentAppVersion;
        review['platform'] = 'Android';
    });

    connectToPython(reviews)
}

const receiver = new AppIdInputReceiver();
receiver.promptUserToFillAppId(receiverCallback);
