var dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.DCC_GraphClickData = function (props) {
    const {setData} = props;
    function setProps() {
        const graphProps = arguments[0];
        if (graphProps['clickData']) {
            setData(graphProps);
        }
    }
    const sectors = props.value.data[0].x
    const navs = props.value.data[0].y

    const labels = sectors.map((sector, ind) => {
        const nav = navs[ind]
        return React.createElement(
            "div",
            { className: "flex justify-between px-4 leading-6" },
            [
                React.createElement("span", { className: "font-bold" }, `${sector}:`),
                React.createElement("span", {}, `${nav}%`)
            ]
        )
    })

    return React.createElement(
        "div",
        { className: "flex flex-col h-full" },
        [
            React.createElement(window.dash_core_components.Graph, {
                figure: props.value,
                setProps,
                style: { width: '100%', height: '150px', marginBottom: "4px" },
                config: {displayModeBar: false},
            }),
            ...labels
        ]
    )
    
};

dagcomponentfuncs.ShowNameAndTicker = function(props) {
    const nameAndTicker = props.value.split(",");
    const name = nameAndTicker[0];
    const ticker = nameAndTicker[1];

    return React.createElement(
        "div", 
        { className: "flex flex-col" },
        [
            React.createElement("span", { className: "text-jade" }, ticker),
            React.createElement("span", { className: "w-full whitespace-normal leading-5 -mt-2" }, name),
        ]
    );
}