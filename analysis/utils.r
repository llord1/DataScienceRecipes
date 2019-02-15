util_libraries = c('moments', 'nortest', 'car')
invisible(lapply(util_libraries, require, character.only = TRUE))
'%nin%' <- function(x,y)!('%in%'(x,y))

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
apa_pvalue <- function(pv) {
  ifelse(
    pv < .001, '< .001',
    ifelse(
      pv < .05, sprintf('= %.3f', pv),
        '> .05'))
} 

#' runs the 5 standard univariate normality tests on every column in the data
test_univariate_normality <- function(data) {
  univariate <- function(data, column) {
    t1 = ad.test(data[, column])
    t2 = cvm.test(data[, column])
    t3 = lillie.test(data[, column])
    t4 = pearson.test(data[, column])
    t5 = sf.test(data[, column])
    
    t2s = function(t) {
      sprintf('%.3f (p = %.2f)',
              unname(t$statistic),
              unname(t$p.value)) }
    
    c(t2s(t1), t2s(t2), t2s(t3), t2s(t4), t2s(t5))
  }
  
  columns <- colnames(data)
  cl <- length(columns)
  tmp <- vector(mode="list", length = cl)
  for(i in 1:cl) { tmp[[i]] <- univariate(data, columns[i]) }
  
  normality <- do.call(rbind, tmp)
  rownames(normality) <- columns
  colnames(normality) <- c('Anderson Darling', 'Cramer von Mises', 'Kolmogorov Smirnov', 'Pearson Chi Square', 'Shapiro Francia')
  normality
}

#' pulls out the (m)anova values into a table
#' https://stackoverflow.com/questions/25898691
lm_to_anova <- function(model, multivariate = F, type = c('II')) {
  
  tests <- c('Pillai', 'Wilks', 'Hotelling-Lawley', 'Roy')
  suppress <- c('(Intercept)', 'Residuals')
  outtests <- car:::print.Anova.mlm
  
  body(outtests)[[16]] <- quote(invisible(tests))
  body(outtests)[[15]] <- NULL
  
  mvf <- function(test_name) {
    result <-
      Anova(
        model,
        type = type,
        multivariate = multivariate,
        test.statistic = test_name)
    if('Anova.mlm' %in% class(result))
      result <- outtests(result)
    result <- result[row.names(result) %nin% suppress,]
    row.names(result) <- sprintf('%s %s', test_name, row.names(result))
    result
  }
  
  tab <- lapply(tests, mvf)
  tab <- do.call(rbind, tab)
  tab
}

