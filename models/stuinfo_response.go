package models

type StuInfoResp struct {
	Meta Meta `json:"meta"`
	Data struct {
		City        string `json:"city"`
		DeclareTime string `json:"declare_time"`
		JnuID       string `json:"jnuId"`
		LocationX   string `json:"location_x"`
		LocationY   string `json:"location_y"`
		Nation      string `json:"nation"`
		Province    string `json:"province"`
		Xbm         string `json:"xbm"`
		Xm          string `json:"xm"`
		Yxsmc       string `json:"yxsmc"`
		Zy          string `json:"zy"`

		MainTable   MainTable   `json:"mainTable"`
		SecondTable SecondTable `json:"secondTable"`
	} `json:"data"`
}
