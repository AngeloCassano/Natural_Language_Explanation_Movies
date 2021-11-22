<!-- External CSS -->
        <link rel="stylesheet" href="../../stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">


        <!-- Fonts -->
        <link href="https://fonts.googleapis.com/css?family=Lato:300,400|Work+Sans:300,400,700" rel="stylesheet">

        <!-- CSS -->
        <link rel="stylesheet" href="../css/style.css">
        <link rel="stylesheet" href="../css/custom.css">
        <link rel="stylesheet" href="http://netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.css">
        
        <script src="https://developer.edamam.com/attribution/badge.js"></script>
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

<style>
#main-container{
        display: flex;
        justify-content: center;
        width: 100%;
}
.card{
        background: white;
        width: 90% !important;
        border: 2px solid aliceblue;
        border-radius: 15px;
        margin: 20px;

}

.card-img-top{
        border-radius: 15px 15px 0px 0px;
        width: 100%;
        height: 300px;
        object-fit: contain;
}

.card-body{
        padding: 10px 20px;
}

.card-title{
        text-align: center;
        width: 100%;
        text-transform: uppercase;
        font-size: 18px;
}

.card-body{
        text-align: center;
}

.ingrediente{
        margin-bottom: 10px;
}

.cards-container{
        display: grid;
        grid-template-columns: 50% 50%;
}
</style>

<?php

session_start();

$film_piaciuti = $_SESSION['film_piaciuti'];
$film_raccomandati = $_SESSION['film_raccomandati'];
$image_film_racc = $_SESSION['image_film_racc'];
$title_film_racc = $_SESSION['title_film_racc'];
$num_proprieta = '3';
$tipo_spiegazione = 'primolivello';
$template = '1';
$html = 'True';



function createURL($film_piaciuti, $film_raccomandati, $num_proprieta, $tipo_spiegazione, $template, $html){
        $url = "http://90.147.102.243:5036/rec/?film_piaciuti=" . $film_piaciuti . "&film_raccomandati=" . $film_raccomandati . "&num_proprieta=" . $num_proprieta . "&tipo_spiegazione=" . $tipo_spiegazione . "&template=" . $template . "&html=" . $html;

        return $url;
}

$request = createURL($film_piaciuti, $film_raccomandati, $num_proprieta, $tipo_spiegazione, $template, $html);
$response  = file_get_contents($request);
$jsonobj  = json_decode($response, true);
//var_dump($jsonobj);
include('head.php');
include('header.php');


if ($jsonobj =='Your preferences are really particular! Sorry, but I can\'t still explain why you received such a recommendation.'){
        $html = '<section id="gtco-single-content" class="bg-white">
                        <div class="container">
                                <div class="section-content blog-content">
                                        <div class="title-wrap">
                                                <br>
                                                <h2 class="section-title">Recommendation for you</h2>
                                                <p class="section-sub-title">'.$jsonobj['explanation'].'</p>
                                        </div>
                                        <div class="col md-1 text-center button-container">
                                                <a href="../html/index.html">
                                                <div class="col-md-8 offset-md-2 form-btn text-center">
                                                        <button id="btnForm" class="btn btn-block btn-secondary btn-red col-md-4 offset-md-4 " type="submit" name="submit" >Return to Home Page</button>
                                                </div> </a>
                                        </div>
                                </div>
                        </div>
                </section>';
        echo($html);
}
else {
        $html = '<section id="gtco-single-content" class="bg-white">
                        <div class="container">
                                <div class="section-content blog-content">
                                        <div class="title-wrap">
                                                <br>
                                                <h2 class="section-title">Recommendation for you</h2>
                                        </div>
                                <div>
                                <div id="main-container">
                                        <div class="card" style="width: 18rem;">
                                                <img src="'.$image_film_racc.'" class="card-img-top" alt="...">
                                                <div class="card-body">
                                                        <br>
                                                        <h5 class="card-title">'.$title_film_racc.'</h5>
                                                        <br>
                                                        <h5 class="card-title">That\'s my third explanation:</h5>
                                                        <p class="card-body">'.$jsonobj['explanation'].'</p>
                                                </div>
                                        </div>
                                </div>
                                <div class="title-wrap">
                                        <br>
                                        <h4 class="section-title">Questionnaire:</h4>
                                </div>
                                <div class="col-md-11 offset-md-1 contact-form-holder mt-4">
                                        <form id="recForm" method="post" action="../php/quest_primolivello.php">
                                            
                                                <div class="form-group row" id="labelPreQuest">
                                                        <label class="col-sm-12 col-form-label">Remember: <u><i>1 Star means completely disagree, 5 Stars mean completely agree</i></u></label>
                                                </div> <br> <br>
                                            
                                                <div class="form-group row" id="Q2div"> <!-- style="display: none;"-->
                                                        <label for="Q2">I understood why this movie was recommended to me</label>
                                                        <fieldset class="rating">  
                                                                                 
                                                                <input type="radio" id="star5Q2" name="Q2" value="5" required/>
                                                                <label for="star5Q2" title="5 - completely agree"></label>
                                                            
                                                                <input type="radio" id="star4Q2" name="Q2" value="4" required/>
                                                                <label class = "full" for="star4Q2" title="4 - agree"></label>
                                                            
                                                                <input type="radio" id="star3Q2" name="Q2" value="3" required/>
                                                                <label class = "full" for="star3Q2" title="3 - neither agree or disagree"></label>
                                                            
                                                                <input type="radio" id="star2Q2" name="Q2" value="2" required/>
                                                                <label class = "full" for="star2Q2" title="2 - disagree"></label>
                                                            
                                                                <input type="radio" id="star1Q2" name="Q2" value="1" required/>
                                                                <label class = "full" for="star1Q2" title="1 - completely disagree"></label>
                                                            
                                                        </fieldset>
                                                </div> <br> <br>
                                            
                                                <div class="form-group row" id="Q3div">    
                                                        <label for="Q3" class="col-sm-6 col-form-label">The explanation made the recommendation more convincing</label>
                                                        <fieldset class="rating">                                   
                                                                <input type="radio" id="star5Q3" name="Q3" value="5" required/>
                                                                <label class = "full" for="star5Q3" title="5 - completely agree"></label>
                                                    
                                                                <input type="radio" id="star4Q3" name="Q3" value="4" required/>
                                                                <label class = "full" for="star4Q3" title="4 - agree"></label>
                                                    
                                                                <input type="radio" id="star3Q3" name="Q3" value="3" required/>
                                                                <label class = "full" for="star3Q3" title="3 - neither agree or disagree"></label>
                                                    
                                                                <input type="radio" id="star2Q3" name="Q3" value="2" required/>
                                                                <label class = "full" for="star2Q3" title="2 - disagree"></label>
                                                    
                                                                <input type="radio" id="star1Q3" name="Q3" value="1" required/>
                                                                <label class = "full" for="star1Q3" title="1 - completely disagree"></label>
                                                        </fieldset>
                                                </div> <br> <br>
                                            
                                                <div class="form-group row" id="Q4div">    
                                                        <label for="Q4" class="col-sm-6 col-form-label">The explanation helped me discover new information about this movie</label>
                                                        <fieldset class="rating">                                   
                                                                <input type="radio" id="star5Q4" name="Q4" value="5" required/>
                                                                <label class = "full" for="star5Q4" title="5 - completely agree"></label>
                                                    
                                                                <input type="radio" id="star4Q4" name="Q4" value="4" required/>
                                                                <label class = "full" for="star4Q4" title="4 - agree"></label>
                                                    
                                                                <input type="radio" id="star3Q4" name="Q4" value="3" required/>
                                                                <label class = "full" for="star3Q4" title="3 - neither agree or disagree"></label>
                                                    
                                                                <input type="radio" id="star2Q4" name="Q4" value="2" required/>
                                                                <label class = "full" for="star2Q4" title="2 - disagree"></label>
                                                    
                                                                <input type="radio" id="star1Q4" name="Q4" value="1" required/>
                                                                <label class = "full" for="star1Q4" title="1 - completely disagree"></label>
                                                        </fieldset>
                                                </div> <br> <br>
                                            
                                                <div class="form-group row" id="Q5div">    
                                                        <label for="Q5" class="col-sm-6 col-form-label">The explanation increased my trust in the recommender system</label>
                                                        <fieldset class="rating">                                   
                                                                <input type="radio" id="star5Q5" name="Q5" value="5" required/>
                                                                <label class = "full" for="star5Q5" title="5 - completely agree"></label>
                                                    
                                                                <input type="radio" id="star4Q5" name="Q5" value="4" required/>
                                                                <label class = "full" for="star4Q5" title="4 - agree"></label>
                                                    
                                                                <input type="radio" id="star3Q5" name="Q5" value="3" required/>
                                                                <label class = "full" for="star3Q5" title="3 - neither agree or disagree"></label>
                                                    
                                                                <input type="radio" id="star2Q5" name="Q5" value="2" required/>
                                                                <label class = "full" for="star2Q5" title="2 - disagree"></label>
                                                    
                                                                <input type="radio" id="star1Q5" name="Q5" value="1" required/>
                                                                <label class = "full" for="star1Q5" title="1 - completely disagree"></label>
                                                        </fieldset>
                                                </div> <br> <br>
                                    
                                                <div class="col md-1 text-center button-container">
                                                        <button id="btnForm" class="btn btn-block btn-secondary btn-red col-md-4 offset-md-4 link-button" type="submit" name="submit">&#x2714   Submit</button>                        
                                                </div> 
                                        </form>
                                </div>
                        </div>
                </section>';
        echo($html);
}

include('footer.php');


?>