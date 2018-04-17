import './NewsPanel.css';

import React from 'react';

import NewsCard from '../NewsCard/NewsCard';

class NewsPanel extends React.Component {
    constructor() {
        super();
        this.state = {
            news: null
        };
    }

    componentDidMount() {
        this.loadMoreNews();
    }

    loadMoreNews(e) {
        this.setState({
            news: [
                {
                    "url": "https://www.wsj.com/articles/berkshire-hathaway-posted-29-billion-gain-in-2017-from-u-s-tax-plan-1519480047",
                    "title": "Berkshire Hathaway Benefits From US Tax Plan",
                    "description": "Berkshire Hathaway posted a $29 billion gain in 2017 related to changes in U.S. tax law, a one-time boost that inflated annual profits for the Omaha conglomerate.",
                    "source": "The Wall Street Journal",
                    "urlToImage": "https://si.wsj.net/public/resources/images/BN-XP717_3812B_TOP_20180224064100.jpg",
                    "digest":"3RjuEomJo26O1syZbU7OHA==\n",
                    "reason": "Recommend"
                },
                {
                    "url": "http://fortune.com/2018/02/23/bitcoin-elon-musk-value/",
                    "title": "Here's How Much Bitcoin Elon Musk Owns",
                    "description": "Tesla CEO Elon Musk isn’t exactly active in cryptocurrency. Musk revealed this week on Twitter how much Bitcoin he owns—and it’s not much.",
                    "source": "fortune",
                    "urlToImage": "https://fortunedotcom.files.wordpress.com/2018/01/elon-musk-tesla-silicon-valley-sex-party.jpg",
                    "digest":"3RjuEomJo26OadyZbU7OHA==\n",
                    "time": "Today",
                    "reason": "Hot"
                }
            ]
        });
    }

    renderNews() {
        var news_list = this.state.news.map(function(news) {
            return (
                // eslint-disable-next-line
                <a className='list-group-item' key={news.digest} href="#">
                    <NewsCard  news={news} />
                </a>
            );
        });

        return (
            <div className="container-fluid">
                <div className="list-group">
                    {news_list}
                </div>
            </div>
        );
    }

    render() {
        if (this.state.news) {
            return (
                <div>{this.renderNews()}</div>
            );
        } else {
            return (
                <div>
                    <div id="msg-app-loading">
                        Loading
                    </div>
                </div>
            );
        }
    }
}

export default NewsPanel;
