import AccountCircleIcon from '@mui/icons-material/AccountCircle'
import AssignmentIcon from '@mui/icons-material/Assignment'
import DateRangeRoundedIcon from '@mui/icons-material/DateRangeRounded'
import EmojiObjectsIcon from '@mui/icons-material/EmojiObjects'
import GroupIcon from '@mui/icons-material/Group'
import { Tab, Tabs } from '@mui/material'
import { Theme } from '@mui/material/styles'
import makeStyles from '@mui/styles/makeStyles'
import React from 'react'
import ContactAmbassadorButton from '../hub/ContactAmbassadorButton'

const useStyles = makeStyles((theme: Theme) => ({
  root: {
    position: 'fixed',
    bottom: 0,
    left: 0,
    right: 0,
    zIndex: 20,
    background: '#f0f2f5',
  },
  tabs: {
    '& .MuiTabs-indicator': {
      backgroundColor: theme.palette.background.default_contrastText,
    },
  },
  tab: {
    color: theme.palette.background.default_contrastText,
  },
}))

export default function MobileBottomMenu({
  tabValue,
  handleTabChange,
  TYPES_BY_TAB_VALUE,
  hubAmbassador,
  hubUrl,
}) {
  const type_icons = {
    projects: AssignmentIcon,
    organizations: GroupIcon,
    events: DateRangeRoundedIcon, // TODO: after updating material-icon to v5+, replace with "CalendarMonthRoundedIcon"
    members: AccountCircleIcon,
    ideas: EmojiObjectsIcon,
  }
  const classes = useStyles()
  return (
    <div className={classes.root}>
      <ContactAmbassadorButton mobile hubAmbassador={hubAmbassador} hubUrl={hubUrl} />
      <>
        <Tabs
          variant="fullWidth"
          value={tabValue}
          onChange={handleTabChange}
          className={classes.tabs}
          centered={true}
        >
          {TYPES_BY_TAB_VALUE.map((t, index) => {
            const tabProps: any = {
              //TODO(unused)  className: classes.tab,
            }
            const typeIcon = {
              icon: type_icons[t],
            }
            return (
              <Tab label={<typeIcon.icon className={classes.tab} />} {...tabProps} key={index} />
            )
          })}
        </Tabs>
      </>
    </div>
  )
}
