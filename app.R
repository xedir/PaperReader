library(pacman)
pacman::p_load(tidyverse, shiny,tsne, ggbiplot, GGally, stream, streamMOA)

pap = read_csv("C:/Users/henke/Documents/results.csv")

uni = unique(pap$paper)
cat = unique(pap$category)

ui = fluidPage(
  titlePanel("SLR - Word occurence"),
  
  sidebarLayout(
    
    sidebarPanel( 
      selectInput(inputId = "paper", label = "Title", choices = uni),
      textOutput('paper0')
    ),
    
    mainPanel(
      
      tabsetPanel( type="tabs",
                   id ="tabs",
                   tabPanel("Simulation Method",dataTableOutput('table5'),plotOutput('plot5')),
                   tabPanel("Phase",dataTableOutput('table0'),plotOutput('plot0')),
                   tabPanel("Disaster",dataTableOutput('table1'),plotOutput('plot1')),
                   tabPanel("Problem",dataTableOutput('table3'),plotOutput('plot3')),
                   tabPanel("Method",dataTableOutput('table2'),plotOutput('plot2')),
                   tabPanel("Simulation Outcome",dataTableOutput('table4'),plotOutput('plot4')), 
                   tabPanel("Simulation Count",dataTableOutput('table6'),plotOutput('plot6')),
                   tabPanel("Test",dataTableOutput('table7'),plotOutput('plot7'))
      )
    )
    
  )
  
)

server = function(input,output,session){
  
  dp0 <- reactive({
    filter(pap,paper == input$paper)%>%
      filter(category == "Phase Phrases")%>%
      select(c("phrase","frequency"))%>%
      arrange(desc(frequency))%>%
      mutate(phrase=factor(phrase, levels=phrase))
  })
  
  dp1 <- reactive({
    filter(pap,paper == input$paper)%>%
      filter(category == "Disaster Phrases")%>%
      select(c("phrase","frequency"))%>%
      arrange(desc(frequency))%>%
      mutate(phrase=factor(phrase, levels=phrase))
    })
  
  dp2 <- reactive({
    filter(pap,paper == input$paper)%>%
      filter(category == "Method Phrases")%>%
      select(c("phrase","frequency"))%>%
      arrange(desc(frequency))%>%
      mutate(phrase=factor(phrase, levels=phrase))
  })
  
  dp3 <- reactive({
    filter(pap,paper == input$paper)%>%
      filter(category == "Problem Phrases")%>%
      select(c("phrase","frequency"))%>%
      arrange(desc(frequency))%>%
      mutate(phrase=factor(phrase, levels=phrase))
  })
  
  dp4 <- reactive({
    filter(pap,paper == input$paper)%>%
      filter(category == "Simulation Outcome Phrases")%>%
      select(c("phrase","frequency"))%>%
      arrange(desc(frequency))%>%
      mutate(phrase=factor(phrase, levels=phrase))
  })
  
  dp5 <- reactive({
    filter(pap,paper == input$paper)%>%
      filter(category == "Simulation Method Phrases")%>%
      select(c("phrase","frequency"))%>%
      arrange(desc(frequency))%>%
      mutate(phrase=factor(phrase, levels=phrase))
  })
  
  dp6 <- reactive({
    filter(pap,paper == input$paper)%>%
      filter(category == "Simulation Count Phrases")%>%
      select(c("phrase","frequency"))%>%
      arrange(desc(frequency))%>%
      mutate(phrase=factor(phrase, levels=phrase))
  })
  
  dp7 <- reactive({
    filter(pap,paper == input$paper)%>%
      filter(category == "Test Phrases")%>%
      select(c("phrase","frequency"))%>%
      arrange(desc(frequency))%>%
      mutate(phrase=factor(phrase, levels=phrase))
  })
  
  
  output$paper0 <- renderText(substr(input$paper,1,nchar(input$paper)-4))
  
  output$table0 <- renderDataTable(dp0())
  output$plot0 <- renderPlot(
    ggplot(dp0(), aes(x=phrase, y=frequency, fill=phrase))+geom_col()+coord_flip()+theme(legend.position = "none", axis.title.y=element_blank())
  )
  
  
  output$table1 <- renderDataTable(dp1())
  output$plot1 <- renderPlot(
    ggplot(dp1(), aes(x=phrase, y=frequency, fill=phrase))+geom_col()+coord_flip()+theme(legend.position = "none", axis.title.y=element_blank())
  )
  
  output$table2 <- renderDataTable(dp2())
  output$plot2 <- renderPlot(
    ggplot(dp2(), aes(x=phrase, y=frequency, fill=phrase))+geom_col()+coord_flip()+theme(legend.position = "none", axis.title.y=element_blank())
  )
  
  output$table3 <- renderDataTable(dp3())
  output$plot3 <- renderPlot(
    ggplot(dp3(), aes(x=phrase, y=frequency, fill=phrase))+geom_col()+coord_flip()+theme(legend.position = "none", axis.title.y=element_blank())
  )
  
  output$table4 <- renderDataTable(dp4())
  output$plot4 <- renderPlot(
    ggplot(dp4(), aes(x=phrase, y=frequency, fill=phrase))+geom_col()+coord_flip()+theme(legend.position = "none", axis.title.y=element_blank())
  )
  
  output$table5 <- renderDataTable(dp5())
  output$plot5 <- renderPlot(
    ggplot(dp5(), aes(x=phrase, y=frequency, fill=phrase))+geom_col()+coord_flip()+theme(legend.position = "none", axis.title.y=element_blank())
  )
  
  output$table6 <- renderDataTable(dp6())
  output$plot6 <- renderPlot(
    ggplot(dp6(), aes(x=phrase, y=frequency, fill=phrase))+geom_col()+coord_flip()+theme(legend.position = "none", axis.title.y=element_blank())
  )
  
  output$table7 <- renderDataTable(dp7())
  output$plot7 <- renderPlot(
    ggplot(dp7(), aes(x=phrase, y=frequency, fill=phrase))+geom_col()+coord_flip()+theme(legend.position = "none", axis.title.y=element_blank())
  )

}

shinyApp(ui=ui, server=server)