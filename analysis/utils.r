#' algorithmly applies the uses the box-cox transform to make a skew of 0
#' originaly from my personal stash of macros
#' https://github.com/markanewman/mnmacros/blob/master/R/apply_bcskew0.r
apply_bcskew0 <- function(x) {
  
  stopifnot(!(missing(x) || is.null(x)))
  stopifnot(is.vector(x) && is.numeric(x))
  lx <- length(x)
  stopifnot(8 <= lx && lx <= 46340)
  stopifnot(x %>% unique() %>% length() > 1)
  
  lb <- -5
  ub <- 5
  step <- 1
  bestlamda <- NA
  bestskew <- Inf
  bestx <- x
  
  if((mx <- min(x)) <= 0) { x <- x - mx + 1 }
  
  for(i in 0:5) {
    
    for(lamda in seq(lb, ub, step) %>% round(i)) {
      
      x2 <- if(lamda == 0) { log(x) } else { x^lamda }
      cs <- (x2 %>% agostino.test())$statistic[1] %>% abs()
      
      if(cs < bestskew) {
        bestskew <- cs
        bestlamda <- lamda
        bestx <- x2
      }
    }
    
    lb <- bestlamda - step
    ub <- bestlamda + step
    step <- step/10
  }
  
  attr(bestx, 'lamda') <- bestlamda
  
  bestx
}

#' converts pvalues into the more familure  '< .05' format
#' originaly from my personal stash of copy/paste macros
pv2str = function(pv) {
  ifelse(
    pv < .0001, '< .0001',
    ifelse(
      pv < .001, '< .001',
      ifelse(
        pv < .01, '< .01',
        ifelse(
          pv < .05, '< .05',
          '> .05'))))
} 