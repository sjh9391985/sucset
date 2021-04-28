const Searching = Search.prototype;

function Search(){
    this.keyword = document.querySelector('input[name = "search"]');
    this.engine = document.querySelector('.SelectSearch');
    this.button = document.querySelector('.img-button');
    this.form = document.querySelector('.search');

    this.Engine();

}

Searching.Engine = function(){
    this.form.addEventListener('submit', e => {

        e.preventDefault();

        let engine = this.engine.value;
        let keyword = this.keyword.value;

        if(engine === 'google'){
            location.href = 'https://www.google.co.kr/search?q=' + keyword;
        } else if(engine ==='naver'){
            location.href = 'https://finance.naver.com/search/search.nhn?query=' + keyword;
        } else if(engine === 'investing'){
            loacation.href = 'https://kr.investing.com/search/?q=' + keyword;
        }
    });
}

new Search();