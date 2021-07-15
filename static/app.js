class BoggleGame{
    constructor(boardId){
    this.board = $(boardId);
    this.words = new Set();
    this.score = 0;
    this.secs = 60;

    this.timer = setInterval(this.counter.bind(this), 1000);


    $('.word-input', this.board).on('submit', this.submitWord.bind(this));
    }

    showMesseage(msg){
        $('.message', this.board).text(msg)

    }

    addWord(word){
        $('.addWord', this.board).append(`<li> ${word} </li> `)
    }

    scoreShow(){
        $('.score', this.board).text(this.score);
    }

    async submitWord(evt){
        evt.preventDefault();
        let wordGet = $('.word', this.board);
        let word = wordGet.val()
        if (this.words.has(word)){
            this.showMesseage("Word already in list")
            }
        const resp = await axios.get("/checkword", {params : {word : word}});
        if (resp.data.result === "not-word"){
            this.showMesseage(`${word} is not a valid English word`);
        }
        else if (resp.data.result === "not-on-board"){
            this.showMesseage(`${word} is not on current board`);
        }
        else{
            this.showMesseage(`YEAAAH. ${word} is on board`);
            this.words.add(word);
            this.addWord(word);
            this.score += word.length;
            this.scoreShow();
            $('.word', this.board).val('')
        }   
    }

    showTimer(){
        $('.timer', this.board).text(this.secs)

    }

    async counter(){
        this.secs -= 1;
        this.showTimer()
        if (this.secs === 0){
            clearInterval(this.timer)
            await this.get_score()
        }
    }

    async get_score(){
        $('.word-input').hide()
        const resp = await axios.post('/score',{ score: this.score})
        if (this.score > resp.data.highscore){
            this.showMesseage(`New Record with score of: ${this.score}`)
        }
        else{
            this.showMesseage(`Your score: ${this.score}`)
        }
    }

    
}

let game = new BoggleGame("#board")