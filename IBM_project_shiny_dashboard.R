
library(shiny)
library(shinydashboard)

library(tidyverse)
library(skimr)
library(janitor)
library(cowplot)
library(plotly)


ui <- dashboardPage(
  dashboardHeader(title = "Techs Dashboard"),
  
  
  dashboardSidebar(
    sidebarMenu(
      
      menuItem("Techs current usage",
               tabName = "current_usage",
               icon = icon("dashboard")),
               
      menuItem("Techs Future Trends",
               tabName = "future_usage",
               icon = icon("clock")),
      
      menuItem("Participants Demographics",
               tabName = "demographics",
               icon = icon("address-book"))
    )
  ),
  
  
  dashboardBody(
    tabItems(
      tabItem(tabName = "current_usage",
        fluidRow(
          column(width = 7,
            fluidRow(box(width = 12, sliderInput("num","Select nÂ° of Technologies",1,10,5))),
            fluidRow(box(width = 12, solidHeader = TRUE, title = "USED WEBFRAMES", status = "primary", plotlyOutput("bubble1", height = 540)))
          ),
          
          column(width = 5,
            fluidRow(box(width = 12, solidHeader = TRUE, title = "USED PROGRAMMING LANGUAGES", status = "primary", plotlyOutput("graph_bar1", height = 300))),
            fluidRow(box(width = 12, solidHeader = TRUE, title = "USED DATABASES", status = "primary", plotlyOutput("graph_bar2", height = 300)))
          )
        )
      ),
      
      
      tabItem(tabName = "future_usage",
         fluidRow(
           column(width = 7,
             fluidRow(box(width = 12, solidHeader = TRUE, sliderInput("num_f",
                                                  "Select nÂ° of Technologies",1,10,5))),
             fluidRow(box(width = 12, solidHeader = TRUE, title = "WANTED WEBFRAMES", status = "primary", plotlyOutput("bubble11", height = 540)))
                  ),
       
           column(width = 5,
             fluidRow(box(width = 12, solidHeader = TRUE, title = "WANTED PROGRAMMING LANGUAGES", status = "primary", plotlyOutput("graph_bar11",
                                                   height = 300))),
             fluidRow(box(width = 12, solidHeader = TRUE, title = "WANTED DATABASES", status = "primary", plotlyOutput("graph_bar22",
                                                   height = 300)))
                 )
               )
         ),
      
      
      tabItem(tabName = "demographics",
              fluidRow(
                column(width = 6,
                  fluidRow(box(width = 12, checkboxGroupInput('check', 
                                                  label = "Select Rapresented Genders",
                                                  choices = c("Man"="Man",
                                                                 "Woman" = "Woman", "Other non-conforming" = "Other non-conforming", "Man non-conforming" = "Man non-conforming", "Woman non-conforming" = "Woman non-conforming", "Woman;Man" = "Woman;Man", "Woman;Man non-conforming" = "Woman;Man non-conforming"), 
                                             selected = c("Man", "Woman"),
                                             inline = TRUE))),
                  fluidRow(box(width = 12, solidHeader = TRUE, title = "RESPONDENTS ED. LEVEL BY GENDER", status = "primary", plotlyOutput("graph_bar31",
                                                                height = 300))
                  )
                ),
                column(width = 6, box(width = 12, solidHeader = TRUE, title = "RESPONDENTS GENDER", status = "primary", plotlyOutput("pie", height = 420)))
              ),
              
              fluidRow(box(width = 12, solidHeader = TRUE, title = "RESPONDENTS AGE", status = "primary", plotlyOutput(("line")))),
            )
    ),
  )
)





server <- function(input, output, session) {
  
 
  
  
df1 <- read.csv("./data/m5_survey_data_demographics.csv")  
df2 <- read.csv("./data/m5_survey_data_technologies_normalised.csv")
  
  


  
#Pagina 1 ______________________________________________________
  output$graph_bar1 <- renderPlotly({
    
    tech_used <- df2 %>% 
      count(LanguageWorkedWith) %>% 
      rename(technology = n) 
    
    tech_used=tech_used[- 1, ]  
    tech_used <- tech_used[order(tech_used$technology, decreasing = TRUE), ]
    row.names(tech_used) <- NULL
    
    
    
    
    plot_ly(head(tech_used, n = input$num), x = ~LanguageWorkedWith,
                     y = ~technology,
                     type = "bar") %>% 
          layout(xaxis = list(categoryorder = "total ascending", tickangle = -45))
    
  })
  
  output$graph_bar2 <- renderPlotly({
    
    db_used <- df2 %>% 
      count(DatabaseWorkedWith) %>% 
      rename(technology = n) 
    
    
    db_used=db_used[- 1, ] 
    db_used <- db_used[order(db_used$technology, decreasing = TRUE), ]
    row.names(db_used) <- NULL  
    
    
    
    
    plot_ly(head(db_used, n = input$num), x = ~DatabaseWorkedWith,
                   y = ~technology,
                   type = "bar") %>% 
        layout(xaxis = list(categoryorder = "total ascending", tickangle = -45))
  })
  
  output$bubble1 <- renderPlotly({
    
    web_used <- df2 %>% 
      count(WebFrameWorkedWith) %>% 
      rename(technology = n) 
    
    
    web_used=web_used[- 1, ] 
    web_used <- web_used[order(web_used$technology, decreasing = TRUE), ]
    row.names(web_used) <- NULL
    
    
    
    
    plot_ly(head(web_used, n = input$num), x = ~WebFrameWorkedWith, y = ~technology,
        text = ~WebFrameWorkedWith,
        type = 'scatter',
        mode = 'markers',
        size = ~technology,
        color = ~technology, colors = 'Spectral',
        #Choosing the range of the bubbles' sizes:
        sizes = c(20, 80),
        marker = list(opacity = 0.8, sizemode = 'diameter')) %>%
  
  layout(title = '',
         xaxis = list(categoryarray = "category ascending", 
                      categoryorder = "array"),
         showlegend = FALSE)
  })
  
  
  
  
  
  
  
  
  
  
  
  
  
  
#Pagina 2_______________________________________________________
output$graph_bar11 <- renderPlotly({
  
  tech_desired <- df2 %>% 
    count(LanguageDesireNextYear) %>% 
    rename(technology = n) 
  
  tech_desired=tech_desired[- 1, ]  
  tech_desired <- tech_desired[order(tech_desired$technology, decreasing = TRUE), ]
  row.names(tech_desired) <- NULL
  
  
  
  
  
  plot_ly(head(tech_desired, n = input$num_f), x = ~LanguageDesireNextYear,
                   y = ~technology,
                   type = "bar") %>% 
        layout(xaxis = list(categoryorder = "total ascending", tickangle = -45))
  
  })

output$graph_bar22 <- renderPlotly({
  
  db_desired <- df2 %>% 
    count(DatabaseDesireNextYear) %>% 
    rename(technology = n) 
  
  
  db_desired=db_desired[- 1, ] 
  db_desired <- db_desired[order(db_desired$technology, decreasing = TRUE), ]
  row.names(db_desired) <- NULL
  
  
  
  
  plot_ly(head(db_desired, n = input$num_f), x = ~DatabaseDesireNextYear,
                   y = ~technology,
                   type = "bar") %>% 
        layout(xaxis = list(categoryorder = "total ascending", tickangle = -45))
  
  })

output$bubble11 <- renderPlotly({
  
  web_desired <- df2 %>% 
    count(WebFrameDesireNextYear) %>% 
    rename(technology = n) 
  
  
  web_desired=web_desired[- 1, ] 
  web_desired <- web_desired[order(web_desired$technology, decreasing = TRUE), ]
  row.names(web_desired) <- NULL
  
  
  
  
  
  plot_ly(head(web_desired, n = input$num_f), 
          x = ~WebFrameDesireNextYear, 
          y = ~technology,
        text = ~WebFrameDesireNextYear,
        type = 'scatter',
        mode = 'markers',
        size = ~technology,
        color = ~technology, colors = 'Spectral',
        #Choosing the range of the bubbles' sizes:
        sizes = c(20, 80),
        marker = list(opacity = 0.8, sizemode = 'diameter')) %>%
  
  layout(title = '',
         xaxis = list(categoryarray = "category ascending", 
                      categoryorder = "array"),
         showlegend = FALSE)
  
  })















#Pagina 3_______________________________________________________


output$graph_bar31 <- renderPlotly({
  
  respond_ed <- df1[ , c("Respondent", "Gender", "EdLevel")]
  respond_ed[respond_ed==""] <- NA
  
  respond_ed <- respond_ed %>%
    drop_na() %>%
    group_by(Gender, EdLevel) %>%
    summarise(tot = n(), .groups = 'keep')
  
  
  
  respond_ed$Gender <- str_replace_all(respond_ed$Gender, c("Man;Non-binary, genderqueer, or gender non-conforming" = "Man non-conforming", "Woman;Non-binary, genderqueer, or gender non-conforming" = "Woman non-conforming", "Woman;Man;Non-binary, genderqueer, or gender non-conforming" = "Woman;Man; non-conforming", "Non-binary, genderqueer, or gender non-conforming" = "Other non-conforming"))
  
  
  
  
  respond_ed[respond_ed == "Bachelorâ€™s degree (BA, BS, B.Eng., etc.)"] <- "Bachelor"
  respond_ed[respond_ed == "Masterâ€™s degree (MA, MS, M.Eng., MBA, etc.)"] <- "Master"
  respond_ed[respond_ed == "Some college/university study without earning a degree"] <- "College, no degree"
  respond_ed[respond_ed == "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)"] <- "Secondary school"
  respond_ed[respond_ed == "Other doctoral degree (Ph.D, Ed.D., etc.)"] <- "Other doctoral degree"
  respond_ed[respond_ed == "Professional degree (JD, MD, etc.)"] <- "Professional degree"
  respond_ed[respond_ed == "I never completed any formal education"] <- "No education"
  respond_ed[respond_ed == "Primary/elementary school"] <- "Primary school"
  
  
  
  
  
  
  dati <- reactive({
    filter(respond_ed, Gender %in% input$check)
  })
  
  
  
  
  plot_ly(dati(), x = ~Gender, y = ~tot, type = 'bar', 
        color = ~EdLevel,
        colors = "RdBu")%>%
  
  layout(yaxis = list(title = 'Count'),
         barmode = 'stack', 
         showlegend=T,
         xaxis = list(tickangle = -45))
  
})



output$pie <- renderPlotly({
  
  respond_gender = df1 %>% 
    count(Gender) %>% 
    rename(tot = n)
  
  respond_gender$Gender <- str_replace_all(respond_gender$Gender, c("Man;Non-binary, genderqueer, or gender non-conforming" = "Man non-conforming", "Woman;Non-binary, genderqueer, or gender non-conforming" = "Woman non-conforming", "Woman;Man;Non-binary, genderqueer, or gender non-conforming" = "Woman;Man; non-conforming", "Non-binary, genderqueer, or gender non-conforming" = "Other non-conforming"))
  
  
  respond_gender=respond_gender[- 1, ] 
  respond_gender <- respond_gender[order(respond_gender$tot, decreasing = TRUE), ]
  
  
  
  
  
  plot_ly(respond_gender, labels = ~Gender, values = ~tot)%>% 
    add_pie(hole = 0.6) 
    #layout(legend = list(x = 0.01, y = 0.99, bgcolor = 'rgba(0,0,0,0)'), height = 300)
  
})

output$line <- renderPlotly({
  
  respond_age <- df1 %>% 
    count(Age) %>% 
    rename(tot = n) %>% 
    drop_na()
  
  
  
  
  plot_ly(respond_age, x = ~Age, y = ~tot, type = 'scatter', mode = 'lines')
  
})
  
}

shinyApp(ui = ui, server = server)


