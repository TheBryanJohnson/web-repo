Rails.application.routes.draw do
# set up 2 routes
  get 'gamestats/search'
  get 'gamestats/index'

# setup the default route to go to the index
  root 'gamestats#index'
 
# setup built-in resources for "gamestats"

  resources :gamestats

end
