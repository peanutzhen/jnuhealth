package models

type MainReq struct {
	Jnuid       string      `json:"jnuid"`
	MainTable   MainTable   `json:"mainTable"`
	SecondTable SecondTable `json:"secondTable"`
}
