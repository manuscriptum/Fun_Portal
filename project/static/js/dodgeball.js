window.onload=function to(){
    function play(){
        var ball = new Array();
        ball[0] = new Ball(150, 150); 
        ball[1] = new Ball(200, 350);
        ball[2] = new Ball(10, 300);
        ball[3] = new Ball(320, 250);
        ball[4] = new Ball(400, 190);
        ball[5] = new Ball(100, 350);
        ball[6] = new Ball(80, 120);
        ball[7] = new Ball(130, 240);

        var player = new Player();

        var score;

        function Player() {
            var x = 10;
            var y = 10;
            var playerColour = "red";
            var width = 25;
            var height = 30;
            var speed = 15;
            this.draw = draw;

            function draw() {
                g.fillStyle = playerColour;
                g.fillRect(x, y, width, height);
                this.isHit();
            }

            this.setX = setX;

            function setX(newX) {
                x = newX;
            }

            this.getX = getX;

            function getX() {
                return x;
            }

            this.setY = setY;

            function setY(newY) {
                y = newY;
            }

            this.getY = getY;

            function getY() {
                return y;
            }

            this.getSpeed = getSpeed;

            function getSpeed() {
                return speed;
            }

            this.getW = getW;

            function getW() {
                return width;
            }

            this.getH = getH;

            function getH() {
                return height;
            }

            this.isHit = isHit;

            function isHit() {
                for (var i = 0; i < ball.length; i++) {
                    if (((x + width) >= ball[i].getX()) && ((x + width) <= (ball[i].getX() + (ball[i].getRadius() * 2))) && ((y + height) >= ball[i].getY()) && ((y + height) <= (ball[i].getY() + (ball[i].getRadius() * 2)))) {
                        clearInterval(theInterval);
                        drawFinalScore();
                    }
                }
            }

        }

        function Ball(newX, newY) {
            var x = newX;
            var y = newY;
            var e = document.getElementById("difficulty");  
            var val = e.options[e.selectedIndex].value
            val=parseInt(val);
            var dx = val;
            var dy = 2*val;
            var radius = 10;
            var targetColour = "blue";
            this.draw = draw;

            function draw() {
                g.beginPath();
                var background = new Image();
                background.src = "http://www.samskirrow.com/background.png";
                g.fillStyle = targetColour;
                g.arc(x, y, radius, 0, Math.PI * 2);
                g.fill();
                g.drawImage(background,0,0);
                g.closePath();
            }

            this.setX = setX;

            function setX(newX) {
                x = newX;
            }

            this.getX = getX;

            function getX() {
                return x;
            }

            this.setY = setY;

            function setY(newY) {
                y = newY;
            }

            this.getY = getY;

            function getY() {
                return y;
            }

            this.getRadius = getRadius;

            function getRadius() {
                return radius;
            }

            this.move = move;

            function move() {
                x += dx;
                y += dy;

                if (x + dx > canvas.width - radius || x + dx < radius) {
                    dx = -dx;
                }
                else if (y + dy < radius) {
                    dy = -dy;
                }
                else if (y + dy > canvas.height - radius) {
                    dy = -dy;
                }
            }

        }

        function playGame() {
            g.clearRect(0, 0, canvas.width, canvas.height); 
            player.draw();

            for (var i = 0; i < 8; i++) {
                ball[i].move();
                ball[i].draw();
            }
            drawElapsedTime();

        }
        var startTime;
        var score;

        function drawElapsedTime() {
            var elapsed = parseInt((new Date() - startTime) / 1000);
            g.save();
            g.beginPath();
            g.fillStyle = "red";
            g.font = "14px Verdana"
            g.globalAlpha = 0.75;
            g.fillText(elapsed + " secs", canvas.width - 75, 25);
            g.restore();
        }

        function drawFinalScore() {
            if (score == null) {
                score = parseInt((new Date() - startTime) / 1000);
            }
            g.save();
            g.beginPath();
            g.fillStyle = "red";
            g.font = "30px Verdana"
            g.fillText("Game Over: " + score + " secs", 50, 35);
            console.log(score);
            g.restore();
    }


    function arrowKeyDown(e) {
        var stepSize = 10; 

        if (e.keyCode == 37) 
        {
            player.setX(player.getX() - player.getSpeed());
            if (player.getX() < 0) {
                player.setX(0);
            }
        } else if (e.keyCode == 38) 
        {
            player.setY(player.getY() - player.getSpeed());
            if (player.getY() < 0) {
                player.setY(0);
            }
        } else if (e.keyCode == 39) 
        {
            player.setX(player.getX() + player.getSpeed());
            if ((player.getX() + player.getW()) > canvas.width) {
                player.setX(canvas.width - player.getW());
            }
        } else if (e.keyCode == 40) 
        {
            player.setY(player.getY() + player.getSpeed());
            if ((player.getY() + player.getH()) > canvas.height) {
                player.setY(canvas.height - player.getH());
            }
        }
    }

    document.addEventListener('keydown', arrowKeyDown);

    var canvas = document.getElementById("simpleCanvas");
    canvas.width = 600;
    canvas.height = 500;

    var g = canvas.getContext("2d");

    startTime = new Date();
    var theInterval = setInterval(playGame, 20);
}  
var el=document.getElementById("select1");
el.addEventListener("click", play, false);
}
window.onbeforeunload= function(event)
{
    var ref=confirm("Confirm Refresh")
    return ref;
}