var dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.DCC_GraphClickData = function (props) {
    const {setData} = props;
    function setProps() {
        const graphProps = arguments[0];
        if (graphProps['clickData']) {
            setData(graphProps);
        }
    }
    return React.createElement(window.dash_core_components.Graph, {
        figure: props.value,
        setProps,
        style: {height: '100%'},
        config: {displayModeBar: false},
    });
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
            React.createElement("span", { className: "-mt-2" }, name),
        ]
    );
}