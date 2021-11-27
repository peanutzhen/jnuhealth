package models

type Meta struct {
	Code      int    `json:"code"`
	Msg       string `json:"msg"`
	Response  string `json:"response"`
	Success   bool   `json:"success"`
	Timestamp string `json:"timestamp"`
}
